from flask_socketio import join_room, leave_room, emit
from flask import render_template, request, session, redirect, url_for

from config import HOST, PORT, UNSAFE_WERKZEUG, DEBUG
from misc import app, socketio, manager, translator, youtube, anilibria


def send_event(room: str, name: str, color: str, sex: str, icon: str, event: str, emit_type: str, time: int = None) -> None:

    translations = {}

    for locale in app.config["LANGUAGES"].keys():
        translations.update({
            locale: render_template(
                "blocks/event.html",
                name=name,
                color=color,
                message=translator.get_event(event, sex, locale),
                icon=icon,
            ),
        })

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": translations[socketio.server.environ[value]["saved_session"]["language"]],
        }
        if time:
            content.update({
                "time": time
            })
        emit(emit_type, content, to=key)


@app.context_processor
def inject_conf_var():
    return dict(
        AVAILABLE_LANGUAGES=app.config["LANGUAGES"],
        CURRENT_LANGUAGE=session.get("language", request.accept_languages.best_match(app.config["LANGUAGES"].keys()))
    )


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        color = request.form.get("nick_color")
        sex = request.form.get("sex")
        links = request.form.get("links")
        code = request.form.get("code")

        data = {
            "code": code,
            "name": name,
            "sex": sex,
            "color": color,
            "links": links,
            "error": {
                "type": "",
                "text": "",
            },
        }

        if not name:

            data["error"]["type"] = "name"
            data["error"]["text"] = translator.get_error("name")
            return render_template("index.html", data=data)

        if request.form.get("join", False) is not False and not code:

            data["error"]["type"] = "code"
            data["error"]["text"] = translator.get_error("code_not_specified")
            return render_template("index.html", data=data)

        room = code

        if request.form.get("create", False) is not False:

            if links[0] == "":
                data["error"]["type"] = "links"
                data["error"]["text"] = translator.get_error("links")
                return render_template("index.html", data=data)

            if "anilibria" in links:
                code = links.split('/')[-1].split('.')[0]
                videos = anilibria.get_links(code)
            else:
                videos = youtube.get_links([links])

            room = manager.generate_room_code(4)
            manager.rooms[room] = {
                "count": 0,
                "links": videos,
                "last_message_id": 1,
                "languages": set()
            }

        elif code not in manager.rooms:

            data["error"]["type"] = "code"
            data["error"]["text"] = translator.get_error("code_not_exist")
            return render_template("index.html", data=data)

        session.update({
            "room": room,
            "name": name,
            "sex": sex,
            "color": color,
        })

        return redirect(url_for("room"))

    return render_template("index.html", data={})


@app.route("/language/<language>")
def set_language(language: str = "en"):
    session.update({"language": language})
    return redirect(request.referrer)


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in manager.rooms:
        return redirect(url_for("index"))

    return render_template("room.html", code=room, links=manager.rooms[room]["links"])


@socketio.on("server_message")
def message(data):
    room = session.get("room")
    name = session.get("name")

    if room not in manager.rooms:
        return

    content = {
        "message": render_template(
            "blocks/message.html",
            name=name,
            color=session.get("color"),
            time=data["time"],
            message=data["message"],
            additional=True if manager.rooms[room].get("last_message") == name and manager.rooms[room]["last_event"] == "message" else False,
            message_id=manager.rooms[room]["last_message_id"]
        ),
        "user": data["user"]
    }

    manager.rooms[room]["last_message"] = name
    manager.rooms[room]["last_message_id"] += 1
    manager.rooms[room]["last_event"] = "message"
    emit("client_message", content, to=room)


@socketio.on("server_play")
def play(data):
    room = session.get("room")
    name = session.get("name")

    if room not in manager.rooms:
        return

    manager.rooms[room]["last_message"] = name
    manager.rooms[room]["last_event"] = "play"

    send_event(
        room, name, session.get("color"), session.get("sex"), "play", "play", "client_play", data["time"]
    )


@socketio.on("server_pause")
def pause():
    room = session.get("room")
    name = session.get("name")

    if room not in manager.rooms:
        return

    manager.rooms[room]["last_message"] = name
    manager.rooms[room]["last_event"] = "pause"

    send_event(
        room, name, session.get("color"), session.get("sex"), "pause", "pause", "client_pause"
    )


@socketio.on("server_seek")
def seek(data):
    room = session.get("room")

    if room not in manager.rooms:
        return

    send_event(
        room, session.get("name"), session.get("color"), session.get("sex"), "seek", "seek", "client_seek", data["time"]
    )


@socketio.on("connect")
def connect():
    room = session.get("room")
    name = session.get("name")

    if room not in manager.rooms:
        leave_room(room)
        return

    join_room(room)

    count = manager.rooms[room]["count"]
    # languages = manager.rooms[room]["languages"].add(session.get("language"))

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "connect",
        "count": count + 1,
    })

    send_event(
        room, name, session.get("color"), session.get("sex"), "bell", "connect", "client_message"
    )


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    # languages = manager.rooms[room]["languages"].remove(session.get("language"))

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "disconnect",
    })

    send_event(
        room, name, session.get("color"), session.get("sex"), "bell", "disconnect", "client_message"
    )

    leave_room(room)
    session.clear()

    if room in manager.rooms:
        manager.rooms[room]["count"] -= 1
        if manager.rooms[room]["count"] <= 0:
            del manager.rooms[room]


@socketio.on("chat_clear")
def chat_clear():
    room = session.get("room")
    manager.rooms[room]["last_event"] = "clear"


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=UNSAFE_WERKZEUG)

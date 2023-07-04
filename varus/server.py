from flask_socketio import join_room, leave_room, emit
from flask import render_template, request, session, redirect, url_for

from json import dumps

from misc import app, socketio, manager, translator, jutsu


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
        link = request.form.get("link")
        code = request.form.get("code")

        data = {
            "code": code,
            "name": name,
            "sex": sex,
            "color": color,
            "link": link,
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

            if link == "":
                data["error"]["type"] = "link"
                data["error"]["text"] = translator.get_error("link")
                return render_template("index.html", data=data)

            room = manager.generate_room_code(4)
            manager.rooms[room] = {
                "count": 0,
                "link": link,
                "last_message_id": 1,
                "last_video_id": 1
            }

        elif code not in manager.rooms:

            data["error"]["type"] = "code"
            data["error"]["text"] = translator.get_error("code_not_exist")
            return render_template("index.html", data=data)

        last_video_id = manager.rooms[room]["last_video_id"]

        if "jut.su" in link:

            jutsu.set_headers({"User-Agent": request.headers.get("User-Agent")})

            seasons = jutsu.get_all_seasons(manager.rooms[room]["link"])
            first_episode = seasons[0].episodes[0]
            episode_links = jutsu.get_episode(first_episode.href)
            manager.rooms[room]["provider"] = {
                "name": "jutsu",
                "data": {
                    "episodes": jutsu.format_seasons(seasons)
                }
            }

            session.update({
                "links": dumps([{
                    "title": first_episode.name,
                    "file": jutsu.format_links(episode_links),
                    "id": last_video_id + 1
                }])
            })

        elif "youtube.com" in link:

            manager.rooms[room]["provider"] = {
                "name": "youtube",
                "data": {}
            }

            session.update({
                "links": dumps([{
                    "title": "YouTube",
                    "file": link,
                    "id": last_video_id + 1
                }])
            })

        session.update({
            "room": room,
            "name": name,
            "sex": sex,
            "color": color,
            "user_agent": request.headers.get("User-Agent")
        })

        manager.rooms[room]["last_video_id"] += 1

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

    return render_template(
        "room.html",
        code=room,
        links=session.get("links"),
        provider=manager.rooms[room]["provider"]
    )


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


@socketio.on("server_change_episode")
def change_episode(data):
    room = session.get("room")
    last_id = manager.rooms[room]["last_video_id"] + 1

    users = []

    for key, value in socketio.server.manager.rooms["/"][room].items():
        jutsu.set_headers({"User-Agent": socketio.server.environ[value]["saved_session"]["user_agent"]})
        links = jutsu.get_episode(data["link"])
        users.append({
            "id": key,
            "content": {
                "links": dumps([{
                    "title": data["name"],
                    "file": jutsu.format_links(links),
                    "id": last_id
                }]),
                "id": last_id
            }
        })

    for user in users:
        emit("client_change_episode", user["content"], to=user["id"])

    manager.rooms[room]["last_video_id"] = last_id

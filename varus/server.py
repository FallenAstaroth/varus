from flask_babel import Babel
from flask_socketio import join_room, leave_room, emit, SocketIO, rooms
from flask import Flask, render_template, request, session, redirect, url_for

from os import path
from json import dumps
from random import choice
from string import ascii_uppercase

from utils import get_label_by_sex, get_error
from config import HOST, PORT, SECRET_KEY, UNSAFE_WERKZEUG, DEBUG, LANGUAGES

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["LANGUAGES"] = LANGUAGES
app.config["BABEL_TRANSLATION_DIRECTORIES"] = path.join(path.abspath(path.dirname(__file__)), "i18n")
socketio = SocketIO(app)

user_rooms = {}


def get_locale():
    language = session.get("language")

    if language:
        return language

    locale = request.accept_languages.best_match(app.config["LANGUAGES"].keys())
    session.update({"language": locale})

    return locale


babel = Babel(app, locale_selector=get_locale)


def generate_unique_code(length):
    while True:
        code = ''.join(choice(ascii_uppercase) for _ in range(length))
        if code in user_rooms:
            continue
        return code


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
        links = request.form.getlist("links")
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
            data["error"]["text"] = get_error("name")
            return render_template("index.html", data=data)

        if request.form.get("join", False) is not False and not code:

            data["error"]["type"] = "code"
            data["error"]["text"] = get_error("code_not_specified")
            return render_template("index.html", data=data)

        room = code

        if request.form.get("create", False) is not False:

            if links[0] == "":
                data["error"]["type"] = "links"
                data["error"]["text"] = get_error("links")
                return render_template("index.html", data=data)

            room = generate_unique_code(4)
            user_rooms[room] = {
                "count": 0,
                "links": dumps([{"title": "123", "file": link} for link in links]),
                "last_message_id": 1,
                "languages": set()
            }

        elif code not in user_rooms:

            data["error"]["type"] = "code"
            data["error"]["text"] = get_error("code_not_exist")
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
    if room is None or session.get("name") is None or room not in user_rooms:
        return redirect(url_for("index"))

    return render_template("room.html", code=room, links=user_rooms[room]["links"])


@socketio.on("server_message")
def message(data):
    room = session.get("room")
    name = session.get("name")

    if room not in user_rooms:
        return

    content = {
        "message": render_template(
            "blocks/message.html",
            name=name,
            color=session.get("color"),
            time=data["time"],
            message=data["message"],
            additional=True if user_rooms[room].get("last_message") == name and user_rooms[room]["last_event"] == "message" else False,
            message_id=user_rooms[room]["last_message_id"]
        ),
        "user": data["user"]
    }

    user_rooms[room]["last_message"] = name
    user_rooms[room]["last_message_id"] += 1
    user_rooms[room]["last_event"] = "message"
    emit("client_message", content, to=room)


@socketio.on("server_play")
def play(data):
    room = session.get("room")
    name = session.get("name")

    if room not in user_rooms:
        return

    events = {}

    for locale in app.config["LANGUAGES"].keys():
        events.update({
            locale: render_template(
                "blocks/event.html",
                name=name,
                color=session.get("color"),
                message=get_label_by_sex("play", session.get("sex"), locale),
                icon="play",
                event="play",
            ),
        })

    user_rooms[room]["last_message"] = name
    user_rooms[room]["last_event"] = "play"

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": events[socketio.server.environ[value]["saved_session"]["language"]],
            "time": data["time"]
        }
        emit("client_play", content, to=key)


@socketio.on("server_pause")
def pause():
    room = session.get("room")
    name = session.get("name")

    if room not in user_rooms:
        return

    events = {}

    for locale in app.config["LANGUAGES"].keys():
        events.update({
            locale: render_template(
                "blocks/event.html",
                name=name,
                color=session.get("color"),
                message=get_label_by_sex("stop", session.get("sex"), locale),
                icon="stop",
                event="pause"
            ),
        })

    user_rooms[room]["last_message"] = name
    user_rooms[room]["last_event"] = "pause"

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": events[socketio.server.environ[value]["saved_session"]["language"]],
        }
        emit("client_pause", content, to=key)


@socketio.on("server_seek")
def seek(data):
    room = session.get("room")

    if room not in user_rooms:
        return

    events = {}

    for locale in app.config["LANGUAGES"].keys():
        events.update({
            locale: render_template(
                "blocks/event.html",
                name=session.get("name"),
                color=session.get("color"),
                message=get_label_by_sex("seek", session.get("sex"), locale),
                icon="seek",
                event="seek"
            ),
        })

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": events[socketio.server.environ[value]["saved_session"]["language"]],
            "time": data["time"]
        }
        emit("client_seek", content, to=key)


@socketio.on("connect")
def connect():
    room = session.get("room")
    name = session.get("name")

    if room not in user_rooms:
        leave_room(room)
        return

    events = {}

    for locale in app.config["LANGUAGES"].keys():
        events.update({
            locale: render_template(
                "blocks/event.html",
                name=name,
                color=session.get("color"),
                message=get_label_by_sex("join", session.get("sex"), locale),
                icon="bell",
                event="connect"
            ),
        })

    join_room(room)

    count = user_rooms[room]["count"]
    # languages = user_rooms[room]["languages"].add(session.get("language"))

    user_rooms[room].update({
        "last_message": name,
        "last_event": "connect",
        "count": count + 1,
    })

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": events[socketio.server.environ[value]["saved_session"]["language"]],
        }
        emit("client_message", content, to=key)


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    events = {}

    for locale in app.config["LANGUAGES"].keys():
        events.update({
            locale: render_template(
                "blocks/event.html",
                name=name,
                color=session.get("color"),
                message=get_label_by_sex("left", session.get("sex"), locale),
                icon="bell"
            ),
        })

    # languages = user_rooms[room]["languages"].remove(session.get("language"))

    user_rooms[room].update({
        "last_message": name,
        "last_event": "disconnect",
    })

    for key, value in socketio.server.manager.rooms["/"][room].items():
        content = {
            "message": events[socketio.server.environ[value]["saved_session"]["language"]],
        }
        emit("client_message", content, to=key)

    leave_room(room)
    session.clear()

    if room in user_rooms:
        user_rooms[room]["count"] -= 1
        if user_rooms[room]["count"] <= 0:
            del user_rooms[room]


@socketio.on("chat_clear")
def chat_clear():
    room = session.get("room")
    user_rooms[room]["last_event"] = "clear"


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=UNSAFE_WERKZEUG)

from flask_socketio import join_room, leave_room, emit, SocketIO
from flask import Flask, render_template, request, session, redirect, url_for

from json import dumps
from random import choice
from string import ascii_uppercase

from utils import get_label_by_sex
from config import HOST, PORT, SECRET_KEY, UNSAFE_WERKZEUG, DEBUG

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app)

rooms = {}


def generate_unique_code(length):
    while True:
        code = ''.join(choice(ascii_uppercase) for _ in range(length))
        if code in rooms:
            continue
        return code


@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
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
            data["error"]["text"] = "Введите имя"
            return render_template("index.html", data=data)

        if request.form.get("join", False) is not False and not code:

            data["error"]["type"] = "code"
            data["error"]["text"] = "Введите код комнаты"
            return render_template("index.html", data=data)

        room = code

        if request.form.get("create", False) is not False:

            if links[0] == "":
                data["error"]["type"] = "links"
                data["error"]["text"] = "Введите ссылку"
                return render_template("index.html", data=data)

            room = generate_unique_code(4)
            rooms[room] = {
                "count": 0,
                "links": dumps([{"title": "123", "file": link} for link in links]),
                "users": {}
            }

        elif code not in rooms:

            data["error"]["type"] = "code"
            data["error"]["text"] = "Такая комната не существует"
            return render_template("index.html", data=data)

        session.update({
            "room": room,
            "name": name,
            "sex": sex,
            "color": color
        })

        return redirect(url_for("room"))

    return render_template("index.html", data={})


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, links=rooms[room]["links"])


@socketio.on("server_message")
def message(data):
    room = session.get("room")
    name = session.get("name")

    if room not in rooms:
        return

    content = {
        "message": render_template(
            "blocks/message.html",
            name=name,
            color=session.get("color"),
            time=data["time"],
            message=data["message"],
            additional=True if rooms[room].get("last_message") == name and rooms[room]["last_event"] == "message" else False
        ),
        "user": data["user"]
    }

    rooms[room]["last_message"] = name
    rooms[room]["last_event"] = "message"
    emit("client_message", content, to=room)


@socketio.on("server_play")
def play(data):
    room = session.get("room")
    name = session.get("name")

    if room not in rooms:
        return

    content = {
        "message": render_template(
            "blocks/event.html",
            name=name,
            color=session.get("color"),
            message=get_label_by_sex("play", session.get("sex")),
            icon="play",
            event="play"
        ),
        "time": data["time"]
    }

    rooms[room]["last_message"] = name
    rooms[room]["last_event"] = "play"
    emit("client_play", content, to=room)


@socketio.on("server_pause")
def pause():
    room = session.get("room")
    name = session.get("name")

    if room not in rooms:
        return

    content = {
        "message": render_template(
            "blocks/event.html",
            name=name,
            color=session.get("color"),
            message=get_label_by_sex("stop", session.get("sex")),
            icon="stop",
            event="pause"
        )
    }

    rooms[room]["last_message"] = name
    rooms[room]["last_event"] = "pause"
    emit("client_pause", content, to=room)


@socketio.on("server_seek")
def seek(data):
    room = session.get("room")

    if room not in rooms:
        return

    content = {
        "message": render_template(
            "blocks/event.html",
            name=session.get("name"),
            color=session.get("color"),
            message=get_label_by_sex("seek", session.get("sex")),
            icon="seek",
            event="seek"
        ),
        "time": data["time"]
    }

    emit("client_seek", content, to=room)


@socketio.on("connect")
def connect():
    room = session.get("room")
    name = session.get("name")

    if room not in rooms:
        leave_room(room)
        return

    content = {
        "message": render_template(
            "blocks/event.html",
            name=name,
            color=session.get("color"),
            message=get_label_by_sex("join", session.get("sex")),
            icon="bell",
            event="connect"
        )
    }

    join_room(room)

    rooms[room]["last_message"] = name
    rooms[room]["last_event"] = "connect"
    rooms[room]["count"] += 1
    emit("client_message", content, to=room)


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["count"] -= 1
        if rooms[room]["count"] <= 0:
            del rooms[room]

    content = {
        "message": render_template(
            "blocks/event.html",
            name=name,
            color=session.get("color"),
            message=get_label_by_sex("left", session.get("sex")),
            icon="bell"
        )
    }

    rooms[room]["last_message"] = name
    rooms[room]["last_event"] = "disconnect"
    emit("client_message", content, to=room)


@socketio.on("chat_clear")
def chat_clear():
    room = session.get("room")
    rooms[room]["last_event"] = "connect"


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=UNSAFE_WERKZEUG)
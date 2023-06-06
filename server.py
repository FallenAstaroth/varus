from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, emit, SocketIO
import random
from json import dumps
from string import ascii_uppercase

from config import HOST, PORT
from utils import get_label_by_sex

app = Flask(__name__)
app.config["SECRET_KEY"] = "varus"
socketio = SocketIO(app)

rooms = {}


def generate_unique_code(length):
    while True:
        code = ''.join(random.choice(ascii_uppercase) for _ in range(length))
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
                "members": 0,
                "messages": [],
                "links": dumps([{"title": "123", "file": link} for link in links])
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

    return render_template("room.html", code=room, messages=rooms[room]["messages"], links=rooms[room]["links"])


@socketio.on("message")
def message(data):
    room = session.get("room")

    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "color":  session.get("color"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)


@socketio.on("play")
def play(data):
    room = session.get("room")

    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "time": data["time"]
    }

    emit("play", content, to=room)


@socketio.on("pause")
def pause(data):
    room = session.get("room")

    if room not in rooms:
        return

    content = {}

    emit("pause", content, to=room)


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    sex = session.get("sex")
    color = session.get("color")

    if not all([room, name, sex]):
        return

    if room not in rooms:
        leave_room(room)
        return

    content = {
        "name": name,
        "color": color,
        "message": f'{get_label_by_sex("join", sex)} к комнате'
    }

    join_room(room)
    send(content, to=room)
    rooms[room]["members"] += 1


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    content = {
        "name": name,
        "color": color,
        "message": f'{get_label_by_sex("left", sex)} комнату'
    }

    send(content, to=room)


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=True, allow_unsafe_werkzeug=True)

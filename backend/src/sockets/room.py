from aiohttp.web import Response

from json import dumps
from typing import Union

from backend.src.misc import socketio, manager, labeler


@socketio.on("server_message")
async def server_message(sid: str, data: dict) -> None:
    """
    Receives a user's message and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")

    content = {
        "user": sid,
        "name": name,
        "color": color,
        "message": data.get("message"),
        "additional": True if manager.rooms[room].get("last_message") == name and manager.rooms[room]["last_event"] == "message" else False,
        "messageId": manager.rooms[room]["last_message_id"],
        "type": "message"
    }

    count = manager.rooms[room]["count"]
    last_message_id = manager.rooms[room]["last_message_id"]

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "message",
        "last_message_id": last_message_id + 1,
        "count": count + 1
    })

    await socketio.emit("client_message", content, room=room)


@socketio.on("server_play")
async def server_play(sid: str, data: dict) -> None:
    """
    Receives the user's play event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "play",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("play", sex),
        "time": data.get("time"),
        "icon": "play",
        "type": "event"
    }

    await socketio.emit("client_play", content, room=room)


@socketio.on("server_pause")
async def server_pause(sid: str) -> None:
    """
    Receives the user's pause event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "pause",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("pause", sex),
        "icon": "pause",
        "type": "event"
    }

    await socketio.emit("client_pause", content, room=room)


@socketio.on("server_seek")
async def server_seek(sid: str, data: dict) -> None:
    """
    Receives the user's seek event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "seek",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("seek", sex),
        "time": data.get("time"),
        "icon": "seek",
        "type": "event"
    }

    await socketio.emit("client_seek", content, room=room)


@socketio.on("server_skip_opening")
async def server_skip_opening(sid: str, data: dict) -> None:
    """
    Receives the user's opening skip event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")
    episode = data.get("id")

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "skip_opening",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("skip", sex),
        "id": episode,
        "icon": "seek",
        "type": "event"
    }

    await socketio.emit("client_skip_opening", content, room=room)


@socketio.on("server_change_episode")
async def server_change_episode(sid: str, data: dict) -> None:
    """
    Receives the user's episode change event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")
    episode = data.get("id")

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "change_episode",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("switch", sex),
        "id": episode,
        "icon": "switch",
        "type": "event"
    }

    await socketio.emit("client_change_episode", content, room=room)


@socketio.on("server_join")
async def server_join(sid: str, data: dict) -> Union[Response, None]:
    """
    Receives the user's join event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - Response|None: Response object with error or None.
    """
    room = data.get("room")
    name = data.get("name")
    color = data.get("color")
    sex = data.get("sex")

    check = await manager.check_room(room)

    if not check:
        content = dumps({
            "description": "Such a room does not exist",
            "type": "code"
        })
        return Response(status=403, body=content, content_type="application/json")

    socketio.enter_room(sid, room)

    user_data = {
        "room": room,
        "name": name,
        "color": color,
        "sex": sex
    }

    await socketio.save_session(sid, user_data)

    count = manager.rooms[room]["count"]

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "connect",
        "count": count + 1,
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("join", sex),
        "icon": "bell",
        "type": "event"
    }

    await socketio.emit("client_message", content, room=room)


@socketio.on("disconnect")
async def disconnect(sid: str) -> None:
    """
    Receives the user's disconnect event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    name = session.get("name")
    color = session.get("color")
    sex = session.get("sex")

    if not manager.rooms.get(room):
        return

    manager.rooms[room].update({
        "last_message": name,
        "last_event": "disconnect",
    })

    content = {
        "name": name,
        "color": color,
        "message": labeler.get_event("left", sex),
        "icon": "bell",
        "type": "event"
    }

    await socketio.emit("client_message", content, room=room)

    socketio.leave_room(sid, room)

    if room in manager.rooms:
        manager.rooms[room]["count"] -= 1
        if manager.rooms[room]["count"] <= 0:
            del manager.rooms[room]


@socketio.on("chat_clear")
async def chat_clear(sid: str) -> None:
    """
    Receives the user's chat clear event.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    session = await socketio.get_session(sid)

    room = session.get("room")
    manager.rooms[room].update({"last_event": "clear"})

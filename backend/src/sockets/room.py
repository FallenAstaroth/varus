from aiohttp.web import Response

from json import dumps
from typing import Union

from backend.src.helpers import User
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
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    if room.get("last_message") == user.name and room["last_event"] == "message":
        additional = True
    else:
        additional = False

    content = {
        "user": sid,
        "name": user.name,
        "color": user.color,
        "message": data.get("message"),
        "additional": additional,
        "messageId": room["last_message_id"],
        "type": "message"
    }

    count = room["count"]
    last_message_id = room["last_message_id"]

    room.update({
        "last_message": user.name,
        "last_event": "message",
        "last_message_id": last_message_id + 1,
        "count": count + 1
    })

    await socketio.emit("client_message", content, room=user.room)


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
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({
        "last_message": user.name,
        "last_event": "play",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("play", user.sex),
        "time": data.get("time"),
        "icon": "play",
        "type": "event"
    }

    await socketio.emit("client_play", content, room=user.room)


@socketio.on("server_pause")
async def server_pause(sid: str) -> None:
    """
    Receives the user's pause event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({
        "last_message": user.name,
        "last_event": "pause",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("pause", user.sex),
        "icon": "pause",
        "type": "event"
    }

    await socketio.emit("client_pause", content, room=user.room)


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
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({
        "last_message": user.name,
        "last_event": "seek",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("seek", user.sex),
        "time": data.get("time"),
        "icon": "seek",
        "type": "event"
    }

    await socketio.emit("client_seek", content, room=user.room)


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
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({
        "last_message": user.name,
        "last_event": "skip_opening",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("skip", user.sex),
        "id": data.get("id"),
        "icon": "seek",
        "type": "event"
    }

    await socketio.emit("client_skip_opening", content, room=user.room)


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
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({
        "last_message": user.name,
        "last_event": "change_episode",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("switch", user.sex),
        "id": data.get("id"),
        "icon": "switch",
        "type": "event"
    }

    await socketio.emit("client_change_episode", content, room=user.room)


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
    user = User(**data)

    check = await manager.check_room(user.room)
    room = manager.rooms[user.room]

    if not check:
        content = dumps({
            "description": "Such a room does not exist",
            "type": "code"
        })

        return Response(status=403, body=content, content_type="application/json")

    socketio.enter_room(sid, user.room)
    await socketio.save_session(sid, user.dict())

    count = room["count"]

    room.update({
        "last_message": user.name,
        "last_event": "connect",
        "count": count + 1,
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("join", user.sex),
        "icon": "bell",
        "type": "event"
    }

    await socketio.emit("client_message", content, room=user.room)


@socketio.on("disconnect")
async def disconnect(sid: str) -> None:
    """
    Receives the user's disconnect event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    try:
        user: User = User(**await socketio.get_session(sid))
    except TypeError:
        return

    room = manager.rooms[user.room]

    if not manager.rooms.get(user.room):
        return

    room.update({
        "last_message": user.name,
        "last_event": "disconnect",
    })

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event("left", user.sex),
        "icon": "bell",
        "type": "event"
    }

    await socketio.emit("client_message", content, room=user.room)
    socketio.leave_room(sid, user.room)

    if user.room in manager.rooms:
        room["count"] -= 1
        if room["count"] <= 0:
            del manager.rooms[user.room]


@socketio.on("chat_clear")
async def chat_clear(sid: str) -> None:
    """
    Receives the user's chat clear event.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    user: User = User(**await socketio.get_session(sid))
    room = manager.rooms[user.room]

    room.update({"last_event": "clear"})

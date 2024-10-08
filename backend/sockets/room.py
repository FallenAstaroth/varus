from utils.dataclasses import User, Room
from misc import socketio, manager, labeler
from utils.enums import UserEvent, ClientEvent, ServerEvent, EventIcon


async def send_event(sid: str, emit_event: ClientEvent, user_event: UserEvent, icon: EventIcon, data: dict = None) -> None:
    """
    Receives play, pause, seek, skip, switch user events and sends them to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - emit_event [str]: Emit event title.
    - user_event [str]: User event title.
    - icon [str]: Event icon.
    - data [dict]: User data.

    Returns:
    - None.
    """
    user: User = User(**await socketio.get_session(sid))
    room: Room = manager.rooms.get(user.room)

    room.messages.last.user = user.name
    room.messages.last.event = user_event

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event(user_event, user.sex),
        "icon": icon,
        "type": "event",
    }

    if user_event in [UserEvent.PLAY, UserEvent.SEEK]:
        content["time"] = data.get("time")

    elif user_event in [UserEvent.SKIP, UserEvent.SWITCH]:
        content["id"] = data.get("id")

    await socketio.emit(emit_event, content, room=user.room)


@socketio.on(ServerEvent.PLAY)
async def server_play(sid: str, data: dict) -> None:
    """
    Receives the user's play event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    await send_event(sid, ClientEvent.PLAY, UserEvent.PLAY, EventIcon.PLAY, data)


@socketio.on(ServerEvent.PAUSE)
async def server_pause(sid: str) -> None:
    """
    Receives the user's pause event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    await send_event(sid, ClientEvent.PAUSE, UserEvent.PAUSE, EventIcon.PAUSE)


@socketio.on(ServerEvent.SEEK)
async def server_seek(sid: str, data: dict) -> None:
    """
    Receives the user's seek event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    await send_event(sid, ClientEvent.SEEK, UserEvent.SEEK, EventIcon.SEEK, data)


@socketio.on(ServerEvent.SKIP)
async def server_skip_opening(sid: str, data: dict) -> None:
    """
    Receives the user's opening skip event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    await send_event(sid, ClientEvent.SKIP, UserEvent.SKIP, EventIcon.SEEK, data)


@socketio.on(ServerEvent.SWITCH)
async def server_change_episode(sid: str, data: dict) -> None:
    """
    Receives the user's episode change event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    await send_event(sid, ClientEvent.SWITCH, UserEvent.SWITCH, EventIcon.SWITCH, data)


@socketio.on(ServerEvent.MESSAGE)
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
    room: Room = manager.rooms.get(user.room)

    if room.messages.last.user == user.name and room.messages.last.event in ["message", "attachment"]:
        additional = True
    else:
        additional = False

    content = {
        "user": sid,
        "name": user.name,
        "color": user.color,
        "message": data.get("message"),
        "additional": additional,
        "messageId": room.messages.last.id,
        "type": "message"
    }

    room.messages.last.id += 1
    room.messages.last.user = user.name
    room.messages.last.event = UserEvent.MESSAGE
    room.messages.count += 1

    await socketio.emit(ClientEvent.MESSAGE, content, room=user.room)


@socketio.on(ServerEvent.ATTACHMENT)
async def server_attachment(sid: str, data: dict) -> None:
    """
    Receives a user's attachment and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - None.
    """
    user: User = User(**await socketio.get_session(sid))
    room: Room = manager.rooms.get(user.room)

    if room.messages.last.user == user.name and room.messages.last.event in ["message", "attachment"]:
        additional = True
    else:
        additional = False

    content = {
        "user": sid,
        "name": user.name,
        "color": user.color,
        "attachment": data.get("attachment"),
        "additional": additional,
        "messageId": room.messages.last.id,
        "type": "attachment"
    }

    room.messages.last.id += 1
    room.messages.last.user = user.name
    room.messages.last.event = UserEvent.ATTACHMENT
    room.messages.count += 1

    await socketio.emit(ClientEvent.ATTACHMENT, content, room=user.room)


@socketio.on(ServerEvent.CONNECT)
async def server_join(sid: str, data: dict) -> None:
    """
    Receives the user's join event and sends it to all users in the room.

    Parameters:
    - sid [str]: Unique user id.
    - data [dict]: User data.

    Returns:
    - Response|None: Response object with error or None.
    """
    user: User = User(**data)
    room: Room = manager.rooms.get(user.room)

    socketio.enter_room(sid, user.room)
    await socketio.save_session(sid, await user.dict())

    room.messages.last.user = user.name
    room.messages.last.event = UserEvent.CONNECT
    room.users.count += 1

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event(UserEvent.CONNECT, user.sex),
        "icon": EventIcon.BELL,
        "type": "event"
    }

    await socketio.emit(ClientEvent.MESSAGE, content, room=user.room)


@socketio.on(ServerEvent.DISCONNECT)
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

    room: Room = manager.rooms.get(user.room)

    if not room:
        return

    room.messages.last.user = user.name
    room.messages.last.event = UserEvent.DISCONNECT

    content = {
        "name": user.name,
        "color": user.color,
        "message": labeler.get_event(UserEvent.DISCONNECT, user.sex),
        "icon": EventIcon.BELL,
        "type": "event"
    }

    await socketio.emit(ClientEvent.MESSAGE, content, room=user.room)
    await manager.subtract_user(user.room)

    socketio.leave_room(sid, user.room)


@socketio.on(ServerEvent.CLEAR)
async def chat_clear(sid: str) -> None:
    """
    Receives the user's chat clear event.

    Parameters:
    - sid [str]: Unique user id.

    Returns:
    - None.
    """
    user: User = User(**await socketio.get_session(sid))
    room: Room = manager.rooms.get(user.room)

    room.messages.last.event = UserEvent.CLEAR

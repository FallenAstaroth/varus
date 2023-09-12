from aiohttp.web import Request, Response

from json import dumps

from backend.src.types.dataclasses import Room
from backend.src.misc import youtube, anilibria, manager


async def create(request: Request) -> Response:
    """
    Creates a new room.

    Parameters:
    - request [Request]: Request object.

    Returns:
    - Response: A Response object.
    """
    form = await request.json()

    link = form.get("link")

    if not link:
        content = dumps({
            "description": "Enter a link",
            "type": "link"
        })

        return Response(status=403, body=content, content_type="application/json")

    if "anilibria" in link:
        code = link.split('/')[-1].split('.')[0]
        videos, skips = await anilibria.get_data(code)
    else:
        videos, skips = await youtube.get_data([link]), None

    code = await manager.create_room(videos)

    content = {
        "room": code,
        "videos": videos
    }

    room: Room = manager.rooms[code]

    if skips:
        room.skips = skips
        content.update({
            "skips": skips
        })

    return Response(status=200, body=dumps(content), content_type="application/json")


async def get(request: Request) -> Response:
    """
    Returns information about the room or an error if it does not exist.

    Parameters:
    - request [Request]: Request object.

    Returns:
    - Response: A Response object.
    """
    form = await request.json()

    code = form.get("code")
    check = await manager.check_room(code)

    if not code or not check:
        content = dumps({
            "description": "Such a room does not exist",
            "type": "code"
        })

        return Response(status=403, body=content, content_type="application/json")

    room: Room = await manager.get_room(code)

    content = dumps({
        "videos": room.videos,
        "skips": room.skips
    })

    return Response(status=200, body=content, content_type="application/json")

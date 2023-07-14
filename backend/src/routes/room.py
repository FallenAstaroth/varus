from aiohttp.web import Request, Response

from json import dumps

from backend.src.misc import youtube, anilibria, manager


async def create(request: Request) -> Response:
    """
    Creates the room.
    :param request: Request
    :return: dict
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
        videos = await anilibria.get_links(code)
    else:
        videos = await youtube.get_links([link])

    room = await manager.create_room(videos)

    content = dumps({
        "room": room,
        "videos": videos
    })

    return Response(status=200, body=content, content_type="application/json")


async def get(request: Request) -> Response:
    """
    Returns the room data.
    :param request: Request
    :return: dict
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

    room = await manager.get_room(code)

    content = dumps({
        "videos": room.get("videos")
    })

    return Response(status=200, body=content, content_type="application/json")

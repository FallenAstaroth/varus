from fastapi import APIRouter
from fastapi.responses import Response

from json import dumps

from backend.src.misc import youtube, anilibria, manager
from backend.src.routes.models import RoomCreateRequest, RoomGetRequest


router = APIRouter(
    prefix="/room",
    tags=["room"]
)


@router.post("/create")
async def room_create(data: RoomCreateRequest):
    if not data.name:
        return Response(
            status_code=403,
            content=dumps({
                "description": "Enter a name",
                "type": "name"
            })
        )

    if not data.link:
        return Response(
            status_code=403,
            content=dumps({
                "description": "Enter a link",
                "type": "link"
            })
        )

    if "anilibria" in data.link:
        code = data.link.split('/')[-1].split('.')[0]
        videos = await anilibria.get_links(code)
    else:
        videos = await youtube.get_links([data.link])

    room = await manager.create_room(videos)

    return Response(
        status_code=200,
        content=dumps({
            "room": room,
            "videos": videos
        })
    )


@router.post("/get")
async def room_get(data: RoomGetRequest):

    check = await manager.check_room(data.code)

    if not data.code or not check:
        return Response(
            status_code=403,
            content=dumps({
                "description": "Such a room does not exist",
                "type": "code"
            })
        )

    room = manager.rooms.get(data.code)

    return Response(
        status_code=200,
        content=dumps({
            "videos": room.get("videos")
        })
    )

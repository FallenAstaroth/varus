from aiohttp import web
from socketio import AsyncServer

from backend.src.modules import RoomsManager, Labeler
from backend.src.providers import Youtube, Anilibria


APP_HOST = "127.0.0.1"
APP_PORT = 5000

ORIGIN = "http://localhost:8080/"

app = web.Application()
socketio = AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
youtube = Youtube()
anilibria = Anilibria()
manager = RoomsManager()
labeler = Labeler()

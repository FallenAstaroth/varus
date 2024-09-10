from aiohttp import web
from socketio import AsyncServer

from modules import RoomsManager, Labeler
from providers import Youtube, Anilibria


app = web.Application()
socketio = AsyncServer(async_mode="aiohttp", cors_allowed_origins="*", max_http_buffer_size=13 * 1024 * 1024)
youtube = Youtube()
anilibria = Anilibria()
manager = RoomsManager()
labeler = Labeler()

from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp

from config import ORIGINS
from backend.src.modules.manager import RoomsManager
from backend.src.providers import Youtube, Anilibria


app = FastAPI()
socketio = AsyncServer(async_mode="asgi", cors_allowed_origins=ORIGINS)
socketio_app = ASGIApp(socketio, other_asgi_app=app)
youtube = Youtube()
anilibria = Anilibria()
manager = RoomsManager()

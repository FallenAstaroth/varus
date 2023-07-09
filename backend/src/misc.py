from fastapi import FastAPI

from backend.src.modules.manager import RoomsManager
from backend.src.providers import Youtube, Anilibria


app = FastAPI()
youtube = Youtube()
anilibria = Anilibria()
manager = RoomsManager()

from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware

from backend.src.misc import app, socketio_app
from backend.src.routes import (
    room as route_room
)
from backend.src.sockets import (
    room as socket_room
)
from backend.src.config import BACKEND_HOST, BACKEND_PORT, BACKEND_RELOAD, BACKEND_WORKERS, ORIGINS


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


async def setup_routes():
    routes = [route_room]
    for route in routes:
        app.include_router(route.router)


@app.on_event("startup")
async def on_startup():
    await setup_routes()


if __name__ == "__main__":
    run("app:socketio_app", host=BACKEND_HOST, port=BACKEND_PORT, workers=BACKEND_WORKERS, reload=BACKEND_RELOAD)

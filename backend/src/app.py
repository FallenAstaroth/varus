from uvicorn import run
from starlette.middleware.cors import CORSMiddleware

from backend.src.misc import app
from backend.src.routes import room
from backend.src.config import BACKEND_HOST, BACKEND_PORT, BACKEND_RELOAD, BACKEND_WORKERS, ORIGINS


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def setup_routes():
    routes = [room]
    for route in routes:
        app.include_router(route.router)


@app.on_event("startup")
async def on_startup():
    await setup_routes()


if __name__ == "__main__":
    run("app:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=BACKEND_RELOAD, workers=BACKEND_WORKERS)

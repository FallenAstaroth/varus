from aiohttp.web import Application

from backend.src.routes import room


def setup(app: Application) -> None:
    """
    Adds for the room namespace.
    :param app: Application
    :return: None
    """
    app.router.add_post("/room/create", room.create)
    app.router.add_post("/room/get", room.get)

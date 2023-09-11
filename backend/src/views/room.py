from aiohttp.web import Application

from backend.src.routes import room


def setup(app: Application) -> None:
    """
    Adds routes for the room page.

    Parameters:
    - app [Application]: Application object.

    Returns:
    - None.
    """
    app.router.add_post("/room/create", room.create)
    app.router.add_post("/room/get", room.get)

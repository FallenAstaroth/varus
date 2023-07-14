from aiohttp.web import Application
from aiohttp_cors import setup as setup_cors, ResourceOptions

from backend.src.views import (
    room as view_room
)
from backend.src.sockets import (
    room as socket_room
)
from backend.src.misc import web, app, socketio, APP_HOST, APP_PORT


def setup_app_sockets(app: Application) -> Application:
    """
    Attaches socket module.
    :return: None
    """
    socketio.attach(app)
    return app


def setup_app_routes(app: Application) -> Application:
    """
    Loads all routers.
    :return: None
    """
    views = [view_room]

    for view in views:
        view.setup(app)

    return app


def setup_app_cors(app: Application) -> Application:
    """
    Setups app CORS.
    :return: None
    """
    cors = setup_cors(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
            allow_methods="*"
        )
    })

    for view in [route for route in app.router.routes() if "/socket.io" not in route.resource.canonical]:
        cors.add(view)

    return app


def run() -> None:
    setup_app_sockets(app)
    setup_app_routes(app)
    setup_app_cors(app)

    web.run_app(
        app,
        host=APP_HOST,
        port=APP_PORT
    )


if __name__ == '__main__':
    run()

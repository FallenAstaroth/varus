from aiohttp.web import Application
from aiohttp_cors import setup as setup_cors, ResourceOptions

from routes import front

from sockets import room
from misc import web, app, socketio
from config import APP_HOST, APP_PORT


def setup_app_sockets(app: Application) -> Application:
    """
    Setups socket module.

    Parameters:
    - app [Application]: Application object.

    Returns:
    - Application: Application object.
    """
    socketio.attach(app)
    return app


def setup_app_routes(app: Application) -> Application:
    """
    Loads all routers.

    Parameters:
    - app [Application]: Application object.

    Returns:
    - Application: Application object.
    """
    app.router.add_routes(front)


def setup_app_cors(app: Application) -> Application:
    """
    Setups CORS module.

    Parameters:
    - app [Application]: Application object.

    Returns:
    - Application: Application object.
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
    """
    Runs the app server.

    Parameters:
    - None.

    Returns:
    - None.
    """
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

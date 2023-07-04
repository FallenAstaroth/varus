from varus.config import HOST, PORT, UNSAFE_WERKZEUG, DEBUG
from varus.misc import app, socketio


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=UNSAFE_WERKZEUG)
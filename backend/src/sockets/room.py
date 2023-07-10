from backend.src.misc import socketio


@socketio.on("connect")
def connect(sid, *args):
    print('connect ', sid)


@socketio.on("disconnect")
def disconnect(sid):
    print('disconnect ', sid)

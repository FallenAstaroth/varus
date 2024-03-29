class UserEvent:
    PLAY = "play"
    PAUSE = "pause"
    SEEK = "seek"
    SKIP = "skip"
    SWITCH = "switch"
    MESSAGE = "message"
    ATTACHMENT = "attachment"
    CLEAR = "clear"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    DEFAULT = "default"


class ClientEvent:
    PLAY = "client_play"
    PAUSE = "client_pause"
    SEEK = "client_seek"
    SKIP = "client_skip_opening"
    SWITCH = "client_change_episode"
    MESSAGE = "client_message"
    ATTACHMENT = "client_attachment"
    DEFAULT = "default"


class ServerEvent:
    PLAY = "server_play"
    PAUSE = "server_pause"
    SEEK = "server_seek"
    SKIP = "server_skip_opening"
    SWITCH = "server_change_episode"
    MESSAGE = "server_message"
    ATTACHMENT = "server_attachment"
    CLEAR = "chat_clear"
    CONNECT = "server_join"
    DISCONNECT = "disconnect"
    DEFAULT = "default"

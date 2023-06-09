$(document).ready(function() {
    let socketio = io();
    let date = new Date();
    let userId = Math.random().toString(36).substring(2, 15);
    console.log(userId)

    function addZero(num) {
        return String(num).padStart(2, '0');
    }

    function cloneChatToOverlay() {
        let newBlock = $(".chat.block")
            .clone()
            .addClass("overlay");
        $("#oframeplayer").append(newBlock);
    }

    let player = new Playerjs({
        id: "player",
        file: JSON.parse($("#player").attr("data-links"))
    });

    cloneChatToOverlay();

    let isInitialPlay = true,
        isInitialPause = true,
        isInitialSeek = true;

    const playerFrame = $("#player"),
          messagesBox = $(".chat-box .messages"),
          messagesScroll = $(".chat-box"),
          chatInputs = $(".chat-inputs");

    const chatScrollToBottom = () => {
        messagesScroll.stop().animate({
            scrollTop: messagesBox.last().prop("scrollHeight")
        }, 300);
    }

    const createMessage = (name, color, message) => {
        messagesBox.append(message);
        chatScrollToBottom();
    };

    const sendMessage = (block) => {
        const messageInput = block.closest(".chat-inputs").find(".message-input");
        const messageText = messageInput.val();

        if (messageText == "") {
            messageInput.focus();
            return;
        }

        socketio.emit("server_message", {
            message: messageText,
            time: `${addZero(date.getHours())}:${addZero(date.getMinutes())}`
        });

        messageInput.val("");
        messageInput.focus();
    };

    socketio.on("client_message", (data) => {
        createMessage(data.name, data.color, data.message);
    });

    socketio.on("client_play", (data) => {
        isInitialPlay = false;
        if (data.user !== userId) {
            if (Math.abs(data.time - player.api("time")) > 1) {
                isInitialSeek = false;
                player.api("seek", data.time);
                console.log("Socket seek: ", data.user);
                isInitialSeek = true;
            }
            if (!player.api("playing")) {
                player.api("play");
                console.log("Socket play: ", data.user);
            }
        }
        createMessage(data.name, data.color, data.message);
        isInitialPlay = true;
    });

    socketio.on("client_pause", (data) => {
        isInitialPause = false;
        if (data.user !== userId) {
            if (player.api("playing")) {
                player.api("pause");
                console.log("Socket pause: ", data.user);
            }
        }
        createMessage(data.name, data.color, data.message);
        isInitialPause = true;
    });

    socketio.on("client_seek", (data) => {
        player.api("seek", data.time);
    });

    chatInputs.on("click", ".message-send", function() {
        sendMessage($(this));
    });

    chatInputs.on("keypress", ".message-input", function(event) {
        if (event.which == 13) {
            sendMessage($(this));
        }
    });

    playerFrame.on("play", (event) => {
        if (isInitialPlay) {
            socketio.emit("server_play", { time: player.api("time"), user: userId });
        } else {
            isInitialPlay = true;
        }
    });

    playerFrame.on("pause", (event) => {
        if (isInitialPause) {
            socketio.emit("server_pause", { user: userId });
        } else {
            isInitialPause = true;
        }
    });

    playerFrame.on("seek", (event) => {
        console.log(1)
        if (isInitialSeek) {
            socketio.emit("server_seek", { time: player.api("time") });
        } else {
            isInitialSeek = true;
        }
    });

    playerFrame.on("fullscreen", () => {
        $(".chat.block.overlay").addClass("active");
        chatScrollToBottom();
    });

    playerFrame.on("exitfullscreen", () => {
        $(".chat.block.overlay").removeClass("active");
        chatScrollToBottom();
    });
});
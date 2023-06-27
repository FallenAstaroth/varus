$(document).ready(function() {
    let socketio = io();
    let date = new Date();
    let userId = Math.random().toString(36).substring(2, 15);

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

    let isInitialPlay = false,
        isInitialPause = false,
        isInitialSeek = false;

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
        isInitialPlay = true;
        if (Math.abs(data.time - player.api("time")) > 1) {
            player.api("seek", data.time);
        }
        if (!player.api("playing")) {
            player.api("play");
        }
        createMessage(data.name, data.color, data.message);
        isInitialPlay = false;
    });

    socketio.on("client_pause", (data) => {
        isInitialPause = true;
        if (player.api("playing")) {
            player.api("pause");
        }
        createMessage(data.name, data.color, data.message);
        isInitialPause = false;
    });

    socketio.on("client_seek", (data) => {
        isInitialSeek = true;
        if (Math.abs(data.time - player.api("time")) > 1) {
            player.api("seek", data.time);
        }
        createMessage(data.name, data.color, data.message);
        isInitialSeek = false;
    });

    chatInputs.on("click", ".message-send", function() {
        sendMessage($(this));
    });

    chatInputs.on("keypress", ".message-input", function(event) {
        if (event.which == 13) {
            sendMessage($(this));
        }
    });

    playerFrame.on("userplay", (event) => {
        if (!isInitialPlay) {
            socketio.emit("server_play", { user: userId, time: player.api("time") });
        } else {
            isInitialPlay = false
        }
    });

    playerFrame.on("pause", (event) => {
        if (!isInitialPause) {
            socketio.emit("server_pause", { user: userId });
        } else {
            isInitialPause = false
        }
    });

    playerFrame.on("userseek", (event) => {
        if (!isInitialSeek) {
            socketio.emit("server_seek", { user: userId, time: player.api("time") });
        } else {
            isInitialSeek = false
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
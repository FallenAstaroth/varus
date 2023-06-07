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

    let isInitialPlay = true,
        isInitialPause = true;

    const playerFrame = $("#player"),
          messagesBox = $(".chat-box .messages"),
          messagesScroll = $(".chat-box"),
          chatInputs = $(".chat-inputs");

    const createMessage = (name, color, message) => {
        messagesBox.append(message);
        messagesScroll.stop().animate({
            scrollTop: messagesBox.last().prop("scrollHeight")
        }, 500);
    };

    const sendMessage = (block) => {
        const messageInput = block.closest(".chat-inputs").find(".message-input");
        const messageText = messageInput.val();

        if (messageText == "") {
            messageInput.focus();
            return;
        }

        socketio.emit("message", {
            message: messageText,
            time: `${addZero(date.getHours())}:${addZero(date.getMinutes())}`
        });

        messageInput.val("");
        messageInput.focus();
    };

    socketio.on("message", (data) => {
        createMessage(data.name, data.color, data.message);
    });

    socketio.on("play", (data) => {
        isInitialPlay = false;
        if (Math.abs(data.time - player.api("time")) > 1) {
            player.api("seek", data.time);
        }
        if (!player.api("playing")) {
            player.api("play");
        }
        createMessage(data.name, data.color, data.message);
        isInitialPlay = true;
    });

    socketio.on("pause", (data) => {
        isInitialPause = false;
        if (player.api("playing")) {
            player.api("pause");
        }
        createMessage(data.name, data.color, data.message);
        isInitialPause = true;
    });

    socketio.on("seek", (data) => {
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
            socketio.emit("play", { time: player.api("time"), user: userId });
        } else {
            isInitialPlay = true;
        }
    });

    playerFrame.on("pause", (event) => {
        if (isInitialPause) {
            socketio.emit("pause", { user: userId });
        } else {
            isInitialPause = true;
        }
    });

//    playerFrame.on("seek", (event) => {
//        socketio.emit("seek", { time: player.api("time") });
//    });

    playerFrame.on("fullscreen", () => {
        $(".chat.block.overlay").addClass("active");
        messagesScroll.stop().animate({
            scrollTop: messagesBox.last().prop("scrollHeight")
        }, 500);
    });

    playerFrame.on("exitfullscreen", () => {
        $(".chat.block.overlay").removeClass("active");
    });
});
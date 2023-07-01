$(document).ready(function() {
    let socketio = io();
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

    const playerFrame = $("#player"),
          messagesBox = $(".chat-box .messages"),
          actionsBox = $(".chat-box .actions"),
          messagesScroll = $(".chat-box"),
          chatInputs = $(".chat-inputs"),
          seekPlus = $("#oframeplayer > pjsdiv:nth-child(21) > pjsdiv:nth-child(3)"),
          seekMinus = $("#oframeplayer > pjsdiv:nth-child(20) > pjsdiv:nth-child(3)"),
          clearButton = $(".chat-clear");

    const chatScrollToBottom = () => {
        messagesScroll.stop().animate({
            scrollTop: messagesBox.last().prop("scrollHeight")
        }, 300);
    }

    const createMessage = (name, color, message, user) => {
        let processedMessage = $(message);
        if (user === userId) {
            processedMessage.addClass("your");
        }
        messagesBox.append(processedMessage);
        chatScrollToBottom();
    };

    const sendMessage = (block) => {
        const messageInput = block.closest(".chat-inputs").find(".message-input");
        const messageText = messageInput.val();

        if (messageText == "") {
            messageInput.focus();
            return;
        }

        let date = new Date();

        socketio.emit("server_message", {
            message: messageText,
            time: `${addZero(date.getHours())}:${addZero(date.getMinutes())}`,
            user: userId
        });

        messageInput.val("");
        messageInput.focus();
    };

    socketio.on("client_message", (data) => {
        createMessage(data.name, data.color, data.message, data.user);
    });

    socketio.on("client_play", (data) => {
        if (Math.abs(data.time - player.api("time")) > 1) {
            player.api("seek", data.time);
        }
        if (!player.api("playing")) {
            player.api("play");
        }
        createMessage(data.name, data.color, data.message, data.user);
    });

    socketio.on("client_pause", (data) => {
        if (player.api("playing")) {
            player.api("pause");
        }
        createMessage(data.name, data.color, data.message, data.user);
    });

    socketio.on("client_seek", (data) => {
        if (Math.abs(data.time - player.api("time")) > 1) {
            player.api("seek", data.time);
        }
        createMessage(data.name, data.color, data.message, data.user);
    });

    chatInputs.on("click", ".message-send", function() {
        sendMessage($(this));
    });

    chatInputs.on("keypress", ".message-input", function(event) {
        if (event.which == 13) {
            sendMessage($(this));
        }
    });

    clearButton.on("click", function() {
        messagesBox.empty();
        socketio.emit("chat_clear");
    });

    playerFrame.on("userplay", () => {
        socketio.emit("server_play", { time: player.api("time") });
    });

    playerFrame.on("userpause", () => {
        socketio.emit("server_pause");
    });

    playerFrame.on("line", (event) => {
        socketio.emit("server_seek", { time: event.originalEvent.info });
    });

    seekPlus.on("click", () => {
        socketio.emit("server_seek", { time: player.api("time") + 15 });
    });

    seekMinus.on("click", () => {
        socketio.emit("server_seek", { time: player.api("time") - 15 });
    });

    playerFrame.on("fullscreen", () => {
        $(".chat.block.overlay").addClass("active");
        chatScrollToBottom();
    });

    playerFrame.on("exitfullscreen", () => {
        $(".chat.block.overlay").removeClass("active");
        chatScrollToBottom();
    });

//    messagesBox.on("click", ".text:not(.event)", () => {
//        actionsBox.fadeIn(200);
//    });
});
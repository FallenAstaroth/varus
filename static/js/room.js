$(document).ready(function() {
    var socketio = io();

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

    let isInitialPlay = true;

    const playerFrame = $("#player"),
          messagesBox = $(".chat-box .messages");
          messagesScroll = $(".chat-box");

    const createMessage = (name, color, msg) => {
        var date = new Date();
        const content = `
        <div class="text">
            <div class="header">
                <p class="name" style="color: ${color}">${name}</p>
                <p class="time">${addZero(date.getHours())}:${addZero(date.getMinutes())}</p>
            </div>
            <p class="message">${msg}</p>
        </div>
        `;
        messagesBox.append(content);
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
            data: messageText
        });

        messageInput.val("");
        messageInput.focus();
    };

    const syncPlayers = (time) => {
        isInitialPlay = false;
        player.api("seek", time);
        player.api("play");
    };

    const sendPlay = () => {
        const time = player.api("time");
        socketio.emit("play", {
            time: time
        });
    };

    const pausePlayers = () => {
        player.api("pause");
    };

    const sendPause = () => {
        socketio.emit("pause", {});
    };

    socketio.on("message", (data) => {
        createMessage(data.name, data.color, data.message);
    });

    socketio.on("play", (data) => {
        syncPlayers(data.time);
    });

    socketio.on("pause", (data) => {
        pausePlayers();
    });

    $(".chat-inputs").on("click", ".message-send", function() {
        sendMessage($(this));
    });

    playerFrame.on("play", (event) => {
        if (isInitialPlay) {
            sendPlay();
        } else {
            isInitialPlay = true;
        }
    });

    $(".chat-inputs").on("keypress", ".message-input", function(event) {
        if (event.which == 13) {
            sendMessage($(this));
        }
    });

    playerFrame.on("pause", () => {
        sendPause();
    });

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
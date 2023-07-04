import { socketio, player } from "./room.js";

$(document).ready(function() {
    const playButton = $("#jutsu-play"),
          episodesSelect = $(".provider.jutsu .episodes");

    playButton.on("click", function() {
        socketio.emit("server_change_episode", { link: episodesSelect.val(), name: episodesSelect.children(":selected").text()});
    });

    socketio.on("client_change_episode", (data) => {
        player.api("push", JSON.parse(data.links));
        player.api("play", `id:${data.id}`);
    });
});
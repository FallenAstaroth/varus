<template>
  <div class="player block">
    <div class="player-frame">
      <div
          class="video"
          id="player"
          @userplay="playEvent"
          @userpause="pauseEvent"
          @line="lineEvent($event)"
          @fullscreen="fullScreenEvent"
          @exitfullscreen="fullScreenExitEvent"
      >
      </div>
    </div>
    <div class="info">
      <h2 class="block-title">Room code: <span class="block-code">code</span></h2>
    </div>
  </div>
</template>

<script>
import {socket} from "@/socket";
import playerjsLoader from "@/assets/js/playerjs-loader";

export default {
  name: "BlockPlayerComponent",
  props: {
    videos: String
  },
  mounted() {
    this.initPlayer();
  },
  methods: {
    playEvent() {
      socket.emit("server_play", {time: window.player.api("time")});
    },
    pauseEvent() {
      socket.emit("server_pause");
    },
    lineEvent(event) {
      socket.emit("server_seek", {time: event.info});
    },
    fullScreenEvent() {
      const chat = document.querySelector(".chat.block.overlay");
      chat.classList.add("active");
      this.$emit("chatChanged");
    },
    fullScreenExitEvent() {
      const chat = document.querySelector(".chat.block.overlay");
      chat.classList.remove("active");
      this.$emit("chatChanged");
    },
    initPlayer() {
      playerjsLoader.then(() => {
        window.player = new window.Playerjs({
          id: "player",
          file: this.videos
        });

        const seekPlus = document.querySelector("#oframeplayer > pjsdiv:nth-child(21) > pjsdiv:nth-child(3)");
        const seekMinus = document.querySelector("#oframeplayer > pjsdiv:nth-child(20) > pjsdiv:nth-child(3)");

        socket.on("client_play", (data) => {
          if (Math.abs(data.time - window.player.api("time")) > 1) {
            window.player.api("seek", data.time);
          }
          if (!window.player.api("playing")) {
            window.player.api("play");
          }
          this.$emit("newMessage", data);
        });

        socket.on("client_pause", (data) => {
          if (window.player.api("playing")) {
            window.player.api("pause");
          }
          this.$emit("newMessage", data);
        });

        socket.on("client_seek", (data) => {
          if (Math.abs(data.time - window.player.api("time")) > 1) {
            window.player.api("seek", data.time);
          }
          this.$emit("newMessage", data);
        });

        seekPlus.addEventListener("click", () => {
          socket.emit("server_seek", {time: window.player.api("time") + 15});
        });

        seekMinus.addEventListener("click", () => {
          socket.emit("server_seek", {time: window.player.api("time") - 15});
        });

        this.$emit("playerCreated");
      });
    },
  }
}
</script>

<style lang="scss" scoped>
.player.block {
  .player-frame {
    height: max-content;
    width: 100%;

    .video {
      width: 100%;
    }
  }

  .info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
  }
}

@media screen and (max-width: 768px) {
  .player.block {
    padding: 0;

    .info {
      margin-top: 0;
      padding: 10px;
    }
  }
}
</style>
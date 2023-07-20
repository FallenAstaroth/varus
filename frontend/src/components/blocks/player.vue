<template>
  <div class="player block">
    <div class="player-frame">
      <div
          class="video"
          id="player"
          @userplay="playEvent"
          @userpause="pauseEvent"
          @userseek="seekEvent"
          @usernew="changeEpisodeEvent"
          @fullscreen="fullScreenEvent"
          @exitfullscreen="fullScreenExitEvent"
      >
      </div>
    </div>
    <div class="info">
      <h2 class="block-title">{{ $t("{0} episode", [title]) }}</h2>
      <div class="actions">
        <button class="btn btn-primary skip" id="skip-opening" @click="skipOpening">
          {{ $t("Skip") }}
        </button>
        <button class="btn btn-primary skip overlay hidden" id="skip-opening-overlay" @click="skipOpening">
          {{ $t("Skip opening") }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import {socket} from "@/socket";
import playerjsLoader from "@/assets/js/playerjs-loader";

export default {
  name: "BlockPlayerComponent",
  props: {
    videos: String,
    skips: Object
  },
  data() {
    return {
      title: null
    }
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
    seekEvent() {
      socket.emit("server_seek", {time: window.player.api("time")});
    },
    skipOpening() {
      socket.emit("server_skip_opening", {id: window.player.api("playlist_id")});
    },
    changeEpisodeEvent() {
      socket.emit("server_change_episode", {id: window.player.api("playlist_id")});
    },
    fullScreenEvent() {
      const chat = document.querySelector(".chat.block.overlay");
      const skip = document.querySelector("#skip-opening-overlay");
      chat.classList.add("active");
      skip.classList.remove("hidden");
      this.$emit("chatChanged");
    },
    fullScreenExitEvent() {
      const chat = document.querySelector(".chat.block.overlay");
      const skip = document.querySelector("#skip-opening-overlay");
      chat.classList.remove("active");
      skip.classList.add("hidden");
      this.$emit("chatChanged");
    },
    getVideoTitle() {
      const title = window.player.api("title");
      if (title) {
        this.title = title.split(" ")[0];
      } else {
        this.title = window.player.api("playlist_title").split(" ")[0];
      }
    },
    addOverlaySkip() {
      const button = document.querySelector(".actions .btn.overlay");
      const player = document.querySelector("#oframeplayer");
      player.appendChild(button);
    },
    initPlayer() {
      playerjsLoader.then(() => {
        window.player = new window.Playerjs({
          id: "player",
          file: this.videos
        });

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

        socket.on("client_skip_opening", (data) => {
          const range = this.skips[window.player.api("playlist_id")];
          if (Math.abs(range[1] - window.player.api("time")) > 1) {
            window.player.api("seek", range[1]);
          }
          this.$emit("newMessage", data);
        });

        socket.on("client_change_episode", (data) => {
          if (window.player.api("playlist_id") !== data.id) {
            window.player.api("find", data.id);
          }
          if (!window.player.api("playing")) {
            window.player.api("play");
          }
          this.getVideoTitle();
          this.$emit("newMessage", data);
        });

        this.addOverlaySkip();
        this.getVideoTitle();

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

    .actions {
      width: 100%;
      max-width: max-content;
      display: flex;
      justify-content: space-between;
      gap: 10px;

      .prev,
      .next {
        img {
          height: 16px;
          width: 16px;
        }
      }

      .skip {
        display: none;
      }
    }
  }
}

.btn {
  &.skip {
    &.overlay {
      display: none;
      position: fixed;
      top: calc(100% - 100px);
      left: 15px;
      transform: translate(0, -50%);
      width: max-content;
      height: max-content;
      background-color: rgba(105, 108, 255, 0.7);
      z-index: 1;
      font-family: "Montserrat", sans-serif;

      &:hover {
        top: calc(100% - 103px);
        transform: translate(0, -50%) !important;
      }

      &.hidden {
        display: none !important;
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .player.block {
    padding: 0;

    .info {
      margin-top: 0;
      padding: 10px;

      .actions {
        gap: 5px;

        .prev,
        .next {
          img {
            height: 10px;
            width: 10px;
          }
        }
      }
    }
  }
}
</style>
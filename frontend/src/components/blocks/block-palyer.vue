<template>
  <div class="player block">
    <div class="player-frame">
      <div
          class="video"
          id="player"
          @play="playEvent"
      >
      </div>
    </div>
    <div class="info">
      <h2 class="block-title">Room code: <span class="block-code">code</span></h2>
    </div>
  </div>
</template>

<script>
import playerjsLoader from "@/assets/js/playerjs-loader";
import { io } from "socket.io-client";

export default {
  name: "BlockPlayerComponent",
  props: {
    videos: String
  },
  setup(props) {
    playerjsLoader.then(() => {
      let player = new window.Playerjs({
        id: "player",
        file: props.videos
      });
      console.log(player);
    });
  },
  mounted() {
    this.socket = io("http://127.0.0.1:5000");
  },
  methods: {
    playEvent() {
      this.socket.emit("connect", () => {
        this.connected = true;
      });
    },
  }
};
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
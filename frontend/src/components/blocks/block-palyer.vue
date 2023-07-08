<template>
  <div class="player block">
    <div class="player-frame">
      <div class="video" id="player" data-links="links"></div>
    </div>
    <div class="info">
      <h2 class="block-title">Room code: <span class="block-code">code</span></h2>
    </div>
  </div>
</template>

<script>
import playerjsLoader from "@/assets/js/playerjs-loader";

export default {
  name: "BlockPlayerComponent",
  setup() {
    playerjsLoader.then(() => {
      let player = new window.Playerjs({
        id: "player",
        file: "https://www.youtube.com/watch?v=fUVJPoStDgo"
      });
      console.log(player);
    });
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
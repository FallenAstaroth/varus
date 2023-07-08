<template>
  <div class="room-page">
    <div class="wrapper">
      <div class="player-chat">
        <BlockPlayer/>
        <BlockChat/>
      </div>
    </div>
  </div>
</template>

<script>
import BlockPlayer from "@/components/blocks/block-palyer";
import BlockChat from "@/components/blocks/block-chat";

export default {
  name: "PageRoomComponent",
  components: {
    BlockPlayer,
    BlockChat
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  max-width: 1440px;
  padding: 20px;
  margin: 0 auto;
  box-sizing: border-box;
}

.player-chat {
  display: flex;
  gap: 20px;
  height: 100%;
}

.room-page {
  height: 100%;
}

@media screen and (max-width: 768px) {
  .player-chat {
    height: 100%;
    flex-direction: column;
    gap: 10px;
  }
}
</style>
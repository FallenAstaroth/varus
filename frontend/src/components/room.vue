<template>
  <div class="room-page">
    <div class="wrapper">
      <div class="player-chat">
        <BlockPlayer v-if="videosReady" :videos="videos"/>
        <BlockChat/>
      </div>
    </div>
  </div>
</template>

<script>
import BlockPlayer from "@/components/blocks/block-palyer";
import BlockChat from "@/components/blocks/block-chat";
import { useRoute } from "vue-router";

export default {
  name: "PageRoomComponent",
  components: {
    BlockPlayer,
    BlockChat
  },
  data() {
    return {
      videos: "",
      videosReady: false
    }
  },
  methods: {
    getVideos() {
      const route = useRoute();
      const params = route.params;
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          {
            code: params.roomId,
          }
        )
      };
      fetch("http://127.0.0.1:5000/room/get", requestOptions)
        .then(response => {
          if (response.status === 403) {
            this.$router.push({ name: "Index" });
            throw new Error("The room does not exist");
          }
          return response.json();
        })
        .then(data => {
          this.videos = data.videos;
          this.videosReady = true;
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  mounted() {
    this.getVideos()
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/items/block";

.room-page {
  height: 100%;

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
}

@media screen and (max-width: 768px) {
  .room-page {
    .player-chat {
      height: 100%;
      flex-direction: column;
      gap: 10px;
    }
  }
}
</style>
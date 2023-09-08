<template>
  <div class="room-page">
    <div class="wrapper">
      <div class="player-chat">
        <Player
            v-if="videosReady"
            :videos="videos"
            :skips="skips"
            @newMessage="newMessage"
            @chatChanged="scrollChatsBottom"
            @playerCreated="playerCreated"
        />
        <Chat
            :messages="messages"
            @chatCreated="chatCreated"
        />
        <Chat
            :messages="messages"
            :chatSwitcher="true"
            @chatCreated="chatCreated"
            class="overlay"
        />
      </div>
    </div>
    <Preloader v-if="!chatStatus || !playerStatus"/>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import {socket} from "@/socket";
import {backendUrl} from "@/globals";
import {colorStorage, nameStorage, sexStorage} from "@/storage";
import Player from "@/components/blocks/player";
import Chat from "@/components/blocks/chat";
import Preloader from "@/components/blocks/preloader";

export default {
  name: "PageRoomComponent",
  components: {
    Player,
    Chat,
    Preloader
  },
  data() {
    return {
      videos: null,
      skips: null,
      videosReady: false,
      messages: [],
      chatStatus: false,
      playerStatus: false
    }
  },
  mounted() {
    this.getVideos();
  },
  computed: {
    blocksReady() {
      return this.chatStatus && this.playerStatus;
    }
  },
  watch: {
    blocksReady(blocksStatus) {
      if (blocksStatus) {
        this.moveChat();
      }
    }
  },
  provide() {
    return {
      messages: this.messages,
    };
  },
  methods: {
    getVideos() {
      const route = useRoute();
      const params = route.params;
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify({code: params.roomId})
      };
      fetch(`${backendUrl}/room/get`, requestOptions)
        .then(response => {
          if (response.status === 403) {
            this.$router.push({name: "Index"});
            throw new Error("The room does not exist");
          }
          return response.json();
        })
        .then(data => {
          this.videos = data.videos;
          this.skips = data.skips;
          this.videosReady = true;
          this.initChat();
          this.initJoin();
        })
        .catch(error => {
          console.error(error);
        });
    },
    initJoin() {
      const userData = {
        "room": this.$route.params.roomId,
        "name": localStorage.getItem(nameStorage),
        "color": localStorage.getItem(colorStorage),
        "sex": localStorage.getItem(sexStorage)
      }
      socket.emit("server_join", userData);
    },
    initChat() {
      socket.on("client_message", (data) => {
        this.newMessage(data);
      });
    },
    playerCreated() {
      this.playerStatus = true;
    },
    chatCreated() {
      this.chatStatus = true;
    },
    newMessage(data) {
      this.messages.push(data);
      this.scrollChatsBottom();
    },
    scrollChatsBottom() {
      const chatBoxes = document.querySelectorAll(".chat-box");
      this.$nextTick(() => {
        chatBoxes.forEach(chatBox => {
          chatBox.scrollTop = chatBox.scrollHeight;
        });
      });
    },
    moveChat() {
      const chat = document.querySelector(".chat.block.overlay");
      const player = document.querySelector("#oframeplayer");
      player.appendChild(chat);
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/items/block";
@import "@/assets/scss/items/chat";

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
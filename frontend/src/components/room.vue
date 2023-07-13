<template>
  <div class="room-page">
    <div class="wrapper">
      <div class="player-chat">
        <Player
            v-if="videosReady"
            :videos="videos"
            @newMessage="newMessage"
        />
        <div class="chat block">
          <div class="top">
            <h2 class="block-title">{{ blockTitle }}</h2>
            <button class="btn btn-primary chat-clear" @click="clearChat">
              <img class="icon" src="@/assets/img/svg/trash.svg" alt=""/>
            </button>
          </div>
          <div class="chat-box" ref="chat">
            <div class="messages">
              <template v-for="(message, index) in messages" :key="index">
                <Event
                    v-if="message.type === 'event'"
                    :color="message.color"
                    :icon="message.icon"
                    :name="message.name"
                    :message="message.message"
                />
                <Message
                    v-else-if="message.type === 'message'"
                    :color="message.color"
                    :name="message.name"
                    :message="message.message"
                    :messageId="message.messageId"
                    :additional="message.additional"
                    :your="message.user === socket.id"
                />
              </template>
            </div>
            <div class="actions">
              <div class="actions-wrapper">
                <span>{{ actionsReply }}</span>
              </div>
            </div>
          </div>
          <div class="chat-inputs">
            <input
                type="text"
                class="form-control message-input"
                :placeholder="inputsMessagePlaceholder"
                name="message"
                autocomplete="off"
                v-model="messageValue"
                @keyup.enter="sendMessage"
                ref="message"
            />
            <button type="button" class="btn btn-primary message-send" name="send" @click="sendMessage">
              <img class="icon" src="@/assets/img/svg/send.svg" alt="">
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import {socket} from "@/socket";
import {colorStorage, nameStorage, sexStorage} from "@/storage";
import Player from "@/components/blocks/player";
import Event from "@/components/items/chat/event";
import Message from "@/components/items/chat/message";

export default {
  name: "PageRoomComponent",
  components: {
    Player,
    Event,
    Message
  },
  computed: {
    socket() {
      return socket
    }
  },
  data() {
    return {
      videos: "",
      videosReady: false,
      blockTitle: "Room chat",
      actionsReply: "Reply",
      inputsMessagePlaceholder: "Message",
      messages: [],
      messageValue: ""
    }
  },
  mounted() {
    this.getVideos();
  },
  methods: {
    getVideos() {
      const route = useRoute();
      const params = route.params;
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(
            {
              code: params.roomId,
            }
        ),
        credentials: "include"
      };
      fetch(`${this.$backendUrl}/room/get`, requestOptions)
          .then(response => {
            if (response.status === 403) {
              this.$router.push({name: "Index"});
              throw new Error("The room does not exist");
            }
            return response.json();
          })
          .then(data => {
            this.videos = data.videos;
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
    sendMessage() {
      if (this.messageValue === "") return;
      socket.emit("server_message", {
        message: this.messageValue
      });
      this.messageValue = "";
      this.$refs.message.focus();
    },
    scrollChatBottom() {
      const container = this.$refs.chat;
      this.$nextTick(() => {
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
    clearChat() {
      this.messages = [];
      socket.emit("chat_clear");
    },
    newMessage(data) {
      this.messages.push(data);
      this.scrollChatBottom();
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

.chat.block {
  max-width: 400px;
  height: 100%;

  .top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .btn {
      height: 30px;
      width: 30px;
      background-color: #35365f;
      border: none;
      box-shadow: none;

      &:hover {
        background-color: #3f406e !important;
      }
    }

    .icon {
      height: 20px;
      width: 20px;
    }
  }

  .block-title {
    margin-top: 0;
  }

  .chat-box {
    position: relative;
    height: calc(100% - 90px);
    margin-bottom: 10px;
    border-top: 1px solid #444564;
    overflow-y: auto;
    padding-right: 10px;
    padding-left: 5px;

    &::-webkit-scrollbar {
      width: 5px;
    }

    &::-webkit-scrollbar-track {
      background: none;
    }

    &::-webkit-scrollbar-thumb {
      background-color: rgba(68, 69, 100, 0);
    }

    &::-webkit-scrollbar-thumb {
      background-color: rgba(68, 69, 100, 1);
    }

    .actions {
      display: none;
      position: absolute;
      color: #a5a5b7;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;

      .actions-wrapper {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        max-width: 70%;
        padding: 10px;
        background-color: rgba(50, 50, 73, 1);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
      }
    }
  }

  .chat-inputs {
    display: flex;
    justify-content: space-between;
    gap: 10px;

    input {
      width: 100%;
    }

    .icon {
      height: 23px;
      width: 23px;
    }
  }
}

.chat.block.overlay {
  display: none;
  position: fixed;
  top: 50%;
  right: 0;
  transform: translate(0, -50%);
  width: 250px;
  height: calc(100% - 200px);
  background-color: rgba(43, 44, 64, .7);
  z-index: 1;
  font-family: 'Montserrat', sans-serif;

  &.active {
    display: block;
  }

  .form-control {
    background-color: rgba(43, 44, 64, .7);
  }

  .btn-primary {
    background-color: rgba(105, 108, 255, .7);
  }

  .top .btn {
    background-color: rgba(53, 54, 95, .7);
  }
}

@media screen and (max-width: 1024px) {
  .chat.block {
    max-width: 300px;
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

  .chat.block {
    max-width: unset;
    overflow: hidden;
    display: flex;
    flex-direction: column;

    .top {
      margin-bottom: 10px;

      .btn {
        height: 20px;
        width: 20px;
        padding: 5px;
        border-radius: 3px;
      }

      .icon {
        height: 13px;
        width: 13px;
      }
    }

    .chat-inputs .icon {
      height: 16px;
      width: 16px;
    }

    .chat-box {
      height: 100%;
      margin-top: 0;
    }

    .block-title {
      padding: 0;
    }
  }

  .chat.block.overlay {
    display: none !important;
  }
}
</style>
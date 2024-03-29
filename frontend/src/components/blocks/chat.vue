<template>
  <div class="chat block">
    <div v-if="chatSwitcher" class="chat-switcher-block">
      <button type="button" class="btn btn-primary chat-switcher" @click="switchChat">
        <img class="icon" src="@/assets/img/svg/right.svg" alt="">
      </button>
    </div>
    <div class="top">
      <h2 class="block-title">{{ $t("Room chat") }}</h2>
      <button class="btn btn-primary chat-clear" @click="clearChat">
        <img class="icon" src="@/assets/img/svg/trash.svg" alt=""/>
      </button>
    </div>
    <div class="chat-box">
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
          <Message
              v-else-if="message.type === 'attachment'"
              :color="message.color"
              :name="message.name"
              :attachment="message.attachment"
              :messageId="message.messageId"
              :additional="message.additional"
              :your="message.user === socket.id"
              @imageClicked="openImage"
          />
        </template>
      </div>
    </div>
    <div class="chat-inputs">
      <div class="inputs">
        <input
          type="text"
          class="form-control message-input"
          :placeholder='$t("Message")'
          name="message"
          autocomplete="off"
          v-model="messageValue"
          @keyup.enter="sendMessage"
          ref="message"
        />
        <input
          type="file"
          id="attach"
          class="form-control attachment-input"
          name="attach"
          accept="image/png, image/jpeg"
          @change="sendAttachment($event)"
        />
        <label for="attach" class="btn btn-transparent attachment-input">
          <img class="icon" src="@/assets/img/svg/attach.svg" alt="">
        </label>
      </div>
      <button type="button" class="btn btn-primary message-send" name="send" @click="sendMessage">
        <img class="icon" src="@/assets/img/svg/send.svg" alt="">
      </button>
    </div>
    <div class="full-image" :class="fullImageHidden" @click="closeImage($event)">
      <div class="image">
        <img class="image-tag" :src="fullImageUrl" alt="">
      </div>
    </div>
  </div>
</template>

<script>
import {socket} from "@/socket";
import Event from "@/components/items/chat/event";
import Message from "@/components/items/chat/message";

export default {
  name: "BlockChatComponent",
  components: {
    Message,
    Event
  },
  props: {
    chatSwitcher: Boolean
  },
  inject: [
      "messages"
  ],
  data() {
    return {
      messageValue: "",
      fullImageHidden: "hidden",
      fullImageUrl: ""
    }
  },
  computed: {
    socket() {
      return socket;
    }
  },
  mounted() {
    this.$emit("chatCreated");
  },
  methods: {
    sendMessage() {
      if (this.messageValue === "") return;
      socket.emit("server_message", {
        message: this.messageValue
      });
      this.messageValue = "";
      this.$refs.message.focus();
    },
    clearChat() {
      socket.emit("chat_clear");
      this.messages.length = 0;
    },
    switchChat() {
      const chat = document.querySelector(".chat.block");

      if (chat.classList.contains("closed")) {
        chat.classList.remove("closed");
      } else {
        chat.classList.add("closed");
      }
    },
    sendAttachment(event) {
      const file = event.target.files[0];
      if (file && file.size / 1024 / 1024 <= 13) {
        socket.emit("server_attachment", {
          attachment: file
        });
      }
    },
    openImage(url) {
      this.fullImageUrl = url;
      this.fullImageHidden = "";
    },
    closeImage() {
      this.fullImageHidden = "hidden";
    }
  }
}
</script>

<style lang="scss" scoped>
.chat.block {
  position: relative;
  max-width: 400px;
  height: 100%;
  transition: .3s ease-in-out;

  .chat-switcher-block {
    position: absolute;
    opacity: 1;
    left: -25px;
    top: 50%;
    transform: translate(0, -50%);
    transition: .3s ease-in-out;

    &.btn-hidden {
      opacity: 0;
    }

    .btn.chat-switcher {
      width: 100%;
      max-width: 25px;
      border-radius: 100px 0 0 100px;
      padding: .175rem;

      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: .3s ease-in-out;
      }
    }
  }

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

    &:hover::-webkit-scrollbar-thumb {
      background-color: rgba(68, 69, 100, 1);
    }
  }

  .chat-inputs {
    display: flex;
    justify-content: space-between;
    gap: 10px;

    .inputs {
      width: 100%;
      position: relative;

      input {
        width: 100%;
        box-sizing: border-box;
      }

      .btn-transparent {
        position: absolute;
        top: 50%;
        right: 7px;
        transform: translate(0, -50%);
      }
    }

    .form-control {
      &.attachment-input {
        display: none;
      }
    }

    .icon {
      height: 23px;
      width: 23px;
    }
  }

  .full-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, .5);
    z-index: 100;

    &.hidden {
      display: none;
    }

    .image {
      width: 100%;
      max-width: max-content;
      height: 100%;
      padding: 6% 20px;
      margin: 0 auto;
      box-sizing: border-box;

      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
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

  &.closed {
    right: -290px;

    .chat-switcher {
      img {
        transform: rotate(180deg);
      }
    }
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
<template>
  <div class="chat block">
    <div class="top">
      <h2 class="block-title">{{ blockTitle }}</h2>
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
  inject: ["messages"],
  data() {
    return {
      blockTitle: "Room chat",
      actionsReply: "Reply",
      inputsMessagePlaceholder: "Message",
      messageValue: ""
    }
  },
  computed: {
    socket() {
      return socket;
    }
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
    }
  }
}
</script>

<style lang="scss" scoped>
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

    &:hover::-webkit-scrollbar-thumb {
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
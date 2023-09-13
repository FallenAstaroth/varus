<template>
  <div class="text" :class="{ 'additional': additional === true, 'your': your === true  }" :data-id="messageId">
    <div class="message-wrapper">
      <div class="header">
        <p class="name" :style="{ color: color }">{{ name }}</p>
        <p class="time">{{ getTime() }}</p>
      </div>
      <p v-if="message" class="message">
        {{ message }}
      </p>
      <div v-if="attachment" class="message">
        <div class="image" @click="imageClicked">
          <img v-if="image" :src="image" alt="">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FormMessageComponent",
  props: {
    color: String,
    name: String,
    message: String,
    attachment: Object,
    messageId: Number,
    additional: Boolean,
    your: Boolean
  },
  data() {
    return {
      image: null,
    }
  },
  mounted() {
    this.image = this.getAttachment(this.attachment);
  },
  methods: {
    addZero(num) {
        return String(num).padStart(2, '0');
    },
    getTime() {
       let date = new Date();
       return `${this.addZero(date.getHours())}:${this.addZero(date.getMinutes())}`;
    },
    getAttachment(attachment) {
      let blob = new Blob([attachment], {type: "image/jpeg"});
      return (window.URL || window.webkitURL).createObjectURL(blob);
    },
    imageClicked() {
      this.$emit("imageClicked", this.image);
    }
  }
}
</script>
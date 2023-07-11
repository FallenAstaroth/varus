<template>
  <div class="text" :class="{ 'additional': additional === true, 'your': your === true  }" :data-id="messageId">
    <div class="message-wrapper">
      <div class="header">
        <p class="name" :style="{ color: color }">{{ name }}</p>
        <p class="time">{{ getTime() }}</p>
      </div>
      <p class="message">{{ message }}</p>
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
    messageId: Number,
    additional: Boolean,
    your: Boolean
  },
  methods: {
    addZero(num) {
        return String(num).padStart(2, '0');
    },
    getTime() {
       let date = new Date();
       return `${this.addZero(date.getHours())}:${this.addZero(date.getMinutes())}`;
    }
  }
}
</script>
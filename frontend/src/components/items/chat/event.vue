<template>
  <div class="text event">
    <p class="message">
        <span class="name" :style="{ color: color }"><img class="icon" :src="require(`@/assets/img/svg/${icon}.svg`)" alt="">{{ name }}</span>
        {{ message }}
    </p>
  </div>
</template>

<script>
export default {
  name: "FormEventComponent",
  props: {
    color: String,
    icon: String,
    name: String,
    message: String
  }
}
</script>
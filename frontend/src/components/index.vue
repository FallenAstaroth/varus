<template>
  <div class="index-page">
    <div class="wrapper">
      <Form/>
    </div>
  </div>
</template>

<script>
import Form from "@/components/forms/create";

export default {
  name: "PageIndexComponent",
  components: {
    Form
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/items/form";

body {
  position: relative;
}

.index-page {
  height: 100%;

  .wrapper {
    width: 100%;
    max-width: 1920px;
    margin: 0 auto;
    padding: 20px;
    display: grid;
    place-items: center;
    overflow-y: auto;
    box-sizing: border-box;
  }
}
</style>
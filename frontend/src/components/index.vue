<template>
  <div class="index-page">
    <div class="wrapper">
      <Form></Form>
    </div>
  </div>
</template>

<script>
import Form from "@/components/forms/form-create-join";

export default {
  name: "PageIndexComponent",
  components: {
    Form
  }
}
</script>

<style lang="scss" scoped>
body {
  position: relative;
}

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

.index-page {
  height: 100%;
}
</style>
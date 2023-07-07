<template>
  <div class="index-page">
    <div class="wrapper">
      <Form></Form>
    </div>
  </div>
</template>

<script>
import Form from "@/components/forms/form";

export default {
  name: "PageIndexComponent",
  components: {
    Form
  }
}
</script>

<style lang="scss">
body {
  position: relative;
}

.wrapper {
  width: 100%;
  max-width: 1920px;
  padding: 20px;
  display: grid;
  place-items: center;
  overflow-y: auto;
  box-sizing: border-box;
}

.index-page {
  height: 100%;

  .rooms.block {
    overflow-y: auto;

    .header h3 {
      margin-bottom: 0;
    }

    .form-inputs {
      margin-top: 1rem;
    }
  }

  form.block {
    max-width: 500px;
  }

  .name-inputs {
    display: flex;
    gap: 10px;

    input[name="name"] {
      flex: 1;
    }
  }

  .btn-create,
  .btn-join {
    width: 100%;
    margin-top: 1rem;
  }
}
</style>
<template>
  <input
      type="color"
      class="form-color-input"
      :name="name"
      :id="id"
      :value="value"
  />
</template>

<script>
export default {
  name: "FormInputColorComponent",
  props: {
    id: String,
    name: String,
    value: String
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/colors";

.form-color-input {
  height: 40px;
  width: 40px;
  min-width: 40px;
  background: transparent;
  border: 1px solid $color-border-default;
  border-radius: 0.375rem;
}

@media screen and (max-width: 768px) {
  .form-color-input {
    height: 32px;
    width: 32px;
  }
}
</style>
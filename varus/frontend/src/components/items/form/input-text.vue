<template>
  <input
      type="text"
      class="form-control"
      :placeholder="placeholder"
      :name="name"
      :id="id"
      :value="value"
      autocomplete="off"
  />
</template>

<script>
export default {
  name: "FormInputTextComponent",
  props: {
    placeholder: String,
    name: String,
    id: String,
    value: String
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/colors";

.form-control {
  display: block;
  padding: 0.4375rem 0.875rem;
  font-size: 0.9375rem;
  font-weight: 400;
  line-height: 1.53;
  color: #a3a4cc;
  background-color: $color-body-background;
  background-clip: padding-box;
  border: 1px solid $color-border-default;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0.375rem;
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
  font-family: "Montserrat", sans-serif;

  &:focus {
    border-color: #696cff;
    background-color: $color-block-background;
    outline: 0;
    box-shadow: 0 0 0.25rem 0.05rem rgba(255, 255, 255, .1);
  }

  &::placeholder {
    padding: 0;
    transition: .3s;
  }

  &:focus::placeholder {
    padding-left: 5px;
  }
}

@media screen and (max-width: 768px) {
  .form-control {
    font-size: 0.7375rem;
    line-height: 1.33;
  }
}
</style>
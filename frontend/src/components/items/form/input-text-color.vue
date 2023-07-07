<template>
  <div class="label-input">
    <Label :id="textId" :text="label"/>
    <div class="name-inputs">
      <input
        type="text"
        class="form-control"
        :placeholder="placeholder"
        :name="textName"
        :id="textId"
        :value="textValue"
        autocomplete="off"
      />
      <input
        type="color"
        class="form-color-input"
        :name="colorName"
        :id="colorId"
        :value="colorValue"
      />
    </div>
  </div>
</template>

<script>
import Label from "@/components/items/form/label";

export default {
  name: "FormInputTextColorComponent",
  components: {
    Label
  },
  props: {
    textId: String,
    textName: String,
    textValue: String,
    placeholder: String,
    colorId: String,
    colorName: String,
    colorValue: String,
    label: String
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
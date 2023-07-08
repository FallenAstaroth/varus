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
        :value="localTextValue"
        :autofocus="focus"
        autocomplete="off"
        @input="updateText"
      />
      <input
        type="color"
        class="form-color-input"
        :name="colorName"
        :id="colorId"
        :value="localColorValue"
        @change="updateColor"
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
    textStorage: String,
    placeholder: String,
    colorId: String,
    colorName: String,
    colorValue: String,
    colorStorage: String,
    label: String,
    focus: Boolean
  },
  data() {
    return {
      localTextValue: this.textValue,
      localColorValue: this.colorValue,
    }
  },
  created() {
    this.localTextValue = localStorage.getItem(this.textStorage) || "";
    this.localColorValue = localStorage.getItem(this.colorStorage) || "#c76ad9";
  },
  methods: {
    updateText(event) {
      localStorage.setItem(this.textStorage, event.target.value);
    },
    updateColor(event) {
      localStorage.setItem(this.colorStorage, event.target.value);
    },
  },
}
</script>

<style lang="scss" scoped>
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
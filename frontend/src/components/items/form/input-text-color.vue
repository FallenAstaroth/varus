<template>
  <div class="label-input">
    <Label :id="textId" :text="label"/>
    <div class="text-clor-input">
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
    this.localTextValue = localStorage.getItem(this.textStorage) || this.textValue;
    this.$emit("textValueUpdated", this.localTextValue);
    this.localColorValue = localStorage.getItem(this.colorStorage) || this.colorValue;
    this.$emit("colorValueUpdated", this.localColorValue);
  },
  methods: {
    updateText(event) {
      let value = event.target.value;
      this.$emit("textValueUpdated", value);
    },
    updateColor(event) {
      let value = event.target.value;
      this.$emit("colorValueUpdated", value);
    },
  }
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

.text-clor-input {
  display: flex;
  gap: 10px;

  input[type="text"] {
    flex: 1;
  }
}

@media screen and (max-width: 768px) {
  .form-color-input {
    height: 32px;
    width: 32px;
  }
}
</style>
<template>
  <div class="label-input">
    <Label :id="id" :text="label"/>
    <input
      type="text"
      class="form-control"
      :placeholder="placeholder"
      :name="name"
      :id="id"
      :value="value"
      autocomplete="off"
    />
  </div>
</template>

<script>
import Label from "@/components/items/form/label";

export default {
  name: "FormInputTextComponent",
  components: {
    Label
  },
  props: {
    id: String,
    name: String,
    value: String,
    placeholder: String,
    label: String
  }
}
</script>
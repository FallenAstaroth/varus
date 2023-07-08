<template>
  <div class="label-input">
    <Label id="" :text="label"/>
    <div :class="classes">
      <div class="form-check form-check-inline" v-for="(item, index) in items" :key="index">
        <input
            type="radio"
            class="form-check-input"
            :name="name"
            :id="item.id"
            :value="item.value"
            :checked="item.checked"
            v-model="selectedOption"
        >
        <label class="form-check-label" :for="item.id">{{ item.text }}</label>
      </div>
    </div>
  </div>
</template>

<script>
import Label from "@/components/items/form/label";

export default {
  name: "FormInputRadioComponent",
  components: {
    Label
  },
  props: {
    classes: String,
    name: String,
    items: Array,
    label: String,
    storage: String
  },
  data() {
    return {
      selectedOption: null,
    }
  },
  mounted() {
    const savedOption = localStorage.getItem(this.storage);
    if (savedOption) this.selectedOption = savedOption;
  },
  watch: {
    selectedOption(value) {
      localStorage.setItem(this.storage, value);
    }
  }
}
</script>

<style lang="scss" scoped>
.form-check {
  display: block;
  min-height: 1.434375rem;
  padding-left: 1.7em;
  margin-bottom: 0.125rem;

  .form-check-input {
    width: 1.2em;
    height: 1.2em;
    margin-top: 0.165em;
    vertical-align: top;
    background-color: #2b2c40;
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    border: 1px solid #444564;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    cursor: pointer;
    float: left;
    margin-left: -1.7em;

    &[type=radio] {
      border-radius: 50%;
    }

    &:checked, &[type=checkbox]:indeterminate {
      background-color: #696cff;
      border-color: #696cff;
      box-shadow: 0 2px 4px 0 rgba(105, 108, 255, .4);
    }

    &:checked[type=radio] {
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='1.5' fill='%23fff'/%3e%3c/svg%3e");
    }
  }

  .form-check-label {
    color: #cbcbe2;
    font-size: 0.9375rem;
    cursor: pointer;
  }
}

.form-check-inline {
  display: inline-block;
  margin-right: 1rem;
}

@media screen and (max-width: 768px) {
  .form-check {
    .form-check-label {
      font-size: 0.8375rem;
    }
  }
}
</style>
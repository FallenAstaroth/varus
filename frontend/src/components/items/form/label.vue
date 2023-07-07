<template>
  <label class="form-label" :for="id">
    {{ text }}
  </label>
</template>

<script>
export default {
  name: "FormLabelComponent",
  props: {
    id: String,
    text: String
  }
}
</script>

<style lang="scss">
.form-label {
  margin-bottom: .5rem;
  font-size: .9rem;
  font-weight: 500;
  color: #cbcbe2;
  font-family: "Montserrat", sans-serif;
}

@media screen and (max-width: 768px) {
  .form-label {
    font-size: .8rem;
  }
}
</style>
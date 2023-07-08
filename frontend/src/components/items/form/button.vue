<template>
  <button
      :type="type"
      :name="name"
      class="btn btn-primary"
  >
    {{ text }}
  </button>
</template>

<script>
export default {
  name: "FormButtonComponent",
  props: {
    type: String,
    name: String,
    text: String
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/numbers";

.btn-primary {
  color: #fff;
  background-color: #696cff;
  border-color: #696cff;
  box-shadow: 0 0.125rem 0.25rem 0 rgba(105, 108, 255, .4);
}

.btn {
  outline: none;
  border: none;
  cursor: pointer;
  font-weight: 400;
  line-height: 1.53;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: $border-radius;
  transition: all .2s ease-in-out;
  padding: 0.4375rem 0.875rem;
  font-size: 0.9375rem;
  font-family: 'Montserrat', sans-serif;

  &:hover {
    color: #fff !important;
    background-color: #5f61e6 !important;
    border-color: #5f61e6 !important;
    transform: translateY(-3px) !important;
    transition: .3s;
  }
}

@media screen and (max-width: 768px) {
  .btn {
    font-size: 0.7375rem;
    line-height: 1.33;
  }
}
</style>
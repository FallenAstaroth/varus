<template>
  <div class="divider">
    <div class="divider-text">{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: "FormDividerComponent",
  props: {
    text: String
  }
}
</script>

<style lang="scss" scoped>
.divider {
  display: block;
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
  margin: 1.5rem 0;

  .divider-text {
    position: relative;
    display: inline-block;
    font-size: .8rem;
    padding: 0 1rem;
    color: #cbcbe2;

    &:before,
    &:after {
      content: "";
      position: absolute;
      top: 50%;
      width: 100vw;
      border-top: 1px solid #444564;
    }

    &:before {
      right: 100%;
    }

    &:after {
      left: 100%;
    }
  }
}

@media screen and (max-width: 768px) {
  .divider {
    margin: 1rem 0;

    .divider-text {
      font-size: .7rem;
    }
  }
}
</style>
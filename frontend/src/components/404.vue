<template>
  <div class="error-page">
    <div class="wrapper">
      <div class="error">
        <div class="image">
          <img src="@/assets/img/404.png" alt="">
        </div>
        <p>{{ $t("Looks like you're lost") }}</p>
        <a href="/" class="btn btn-primary btn-home">{{ $t("Back to Home") }}</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Page404Component"
}
</script>

<style lang="scss">
body {
  position: relative;
}

.error-page {
  height: 100%;

  .wrapper {
    width: 100%;
    max-width: 1920px;
    margin: 0 auto;
    padding: 20px;
    display: grid;
    place-items: center;
    overflow-y: auto;
    box-sizing: border-box;
  }

  .error {
    width: 100%;
    max-width: max-content;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .image {
      width: 100%;
      max-width: 256px;

      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }

    p {
      font-weight: 700;
      color: #cbcbe2;
      font-size: 1.375rem;
      text-align: center;
    }

    .btn-home {
      margin: 20px auto;
    }
  }
}

@media screen and (max-width: 768px) {
  .error-page {
    .error {
      .image {
        max-width: 200px;
      }

      p {
        font-size: 1rem;
      }
    }
  }
}
</style>
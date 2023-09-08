<template>
  <div class="preloader">
    <div class="wrapper">
      <div class="image">
        <img src="@/assets/img/preloader.png" alt="Preloader">
      </div>
      <p>{{ $t("Almost done") }}</p>
      <div class="spinner">
        <div class="blob top"></div>
        <div class="blob bottom"></div>
        <div class="blob left"></div>
        <div class="blob move-blob"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlockPreloaderComponent"
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/colors";

body {
  position: relative;
}

.preloader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: $color-body-background;
  z-index: 100;

  .wrapper {
    width: 100%;
    max-width: 1920px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    overflow-y: auto;
    box-sizing: border-box;
  }

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

  .spinner {
    width: 28px;
    height: 28px;
    position: relative;
    margin-top: 20px;

    .blob {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border: 2px solid #696cff;
      width: 8px;
      height: 8px;
      border-radius: 50%;

      &.top {
        top: 0;
        animation: blob-top 1s infinite ease-in;
      }

      &.bottom {
        top: 100%;
         animation: blob-bottom 1s infinite ease-in;
      }

      &.left {
        left: 0;
        animation: blob-left 1s infinite ease-in;
      }
    }

    .move-blob {
      background: #696cff;
      top: 0;
      animation: blob-spinner-mover 1s infinite ease-in;
    }
  }

  @keyframes blob-bottom {
    25%, 50%, 75% {
      top: 50%;
      left: 100%;
    }

    100% {
      top: 0;
      left: 50%;
    }
  }

  @keyframes blob-left {
    25% {
      top: 50%;
      left: 0;
    }

    50%, 100% {
      top: 100%;
      left: 50%;
    }
  }

  @keyframes blob-top {
    50% {
      top: 0;
      left: 50%;
    }

    75%, 100% {
      top: 50%;
      left: 0;
    }
  }

  @keyframes blob-spinner-mover {
    0%, 100% {
      top: 0;
      left: 50%;
    }

    25% {
      top: 50%;
      left: 100%;
    }

    50% {
      top: 100%;
      left: 50%;
    }

    75% {
      top: 50%;
      left: 0;
    }
  }
}

@media screen and (max-width: 768px) {
  .preloader {
    .image {
      max-width: 200px;
    }

    p {
      font-size: 1rem;
    }

    .spinner {
      width: 25px;
      height: 25px;
      margin-top: 15px;

      .blob {
        width: 6px;
        height: 6px;
      }
    }
  }
}
</style>
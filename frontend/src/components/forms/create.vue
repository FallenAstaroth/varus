<template>
  <form method="post" class="rooms block">
    <div class="header">
      <h3 class="form-title">
        <div class="logo">
          <img src="@/assets/img/svg/logo.svg" alt=""/>
        </div>
        {{ formTitle }}
      </h3>
    </div>
    <div class="form-inputs">
      <InputText
          id="link"
          name="link"
          value=""
          :placeholder='$t("YouTube, Anilibria or file")'
          :label='$t("Link")'
          @textValueUpdated="updateLink"
      />
      <button type="button" name="create" class="btn btn-primary btn-create" @click="sendCreate">
        {{ $t("Create a room") }}
      </button>
    </div>
  </form>
</template>

<script>
import {backendUrl} from "@/globals";
import InputText from "@/components/items/form/input-text";

export default {
  name: "FormComponent",
  components: {
    InputText
  },
  data() {
    return {
      formTitle: "arus"
    }
  },
  methods: {
    updateLink(value) {
      this.localLinkValue = value;
    },
    sendCreate() {
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify({link: this.localLinkValue})
      };
      fetch(`${backendUrl}/room/create`, requestOptions)
        .then(response => {
          if (response.status === 403) {
            this.$router.push({name: "Index"});
            throw new Error("Error");
          }
          return response.json();
        })
        .then(data => {
          this.$router.push({name: "Room", params: {roomId: data.room}});
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>

<style lang="scss" scoped>
.rooms.block {
  overflow-y: auto;
  max-width: 500px;

  .header h3 {
    margin-bottom: 0;
  }

  .form-inputs {
    margin-top: 1rem;
  }

  .form-title {
    margin-bottom: 1rem;
    font-weight: 700;
    line-height: 1.1;
    color: #cbcbe2;
    font-size: 1.375rem;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;

    .logo {
      width: 100%;
      max-width: 30px;
      height: 100%;
      max-height: 30px;

      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }
  }

  .btn-create,
  .btn-join {
    width: 100%;
    margin-top: 1rem;
  }
}

@media screen and (max-width: 768px) {
  .rooms.block {
    .form-title {
      line-height: 1;
      font-size: 1.175rem;
      margin-bottom: 0;

      .logo {
        max-width: 25px;
        max-height: 25px;
      }
    }
  }
}
</style>
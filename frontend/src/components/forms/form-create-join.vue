<template>
  <form method="post" class="rooms block">
    <div class="header">
      <h3 class="form-title">{{ formTitle }}</h3>
    </div>
    <div class="form-inputs">
      <InputTextColor
          text-id="name"
          text-name="name"
          :text-value="nameValue"
          text-storage="createJoinUserName"
          color-id="color"
          color-name="color"
          :color-value="colorValue"
          color-storage="createJoinUserColor"
          :placeholder="namePlaceholder"
          :label="nameTitle"
          focus
          @textValueUpdated="updateName"
          @colorValueUpdated="updateColor"
      />
      <InputRadio
          classes="sexes"
          name="sex"
          :items="sexItems"
          :label="sexTitle"
          storage="createJoinSex"
          @radioValueUpdated="updateSex"
      />
      <Divider :text="dividerCreate"/>
      <InputText
          id="link"
          name="link"
          value=""
          :placeholder="linkPlaceholder"
          :label="linkTitle"
          @textValueUpdated="updateLink"
      />
      <button type="button" name="create" class="btn btn-primary btn-create" @click="sendCreate">
        {{ createButton }}
      </button>
    </div>
  </form>
</template>

<script>
import InputText from "@/components/items/form/input-text";
import InputTextColor from "@/components/items/form/input-text-color";
import InputRadio from "@/components/items/form/input-radio";
import Divider from "@/components/items/form/divider";

export default {
  name: "FormComponent",
  components: {
    InputText,
    InputTextColor,
    InputRadio,
    Divider
  },
  data() {
    return {
      formTitle: "Varus TV",
      nameTitle: "Name",
      namePlaceholder: "Johnny Depp",
      nameValue: "",
      colorValue: "#c76ad9",
      sexTitle: "Sex",
      sexItems: [
        {id: "male", value: "male", text: "Male", checked: true},
        {id: "female", value: "female", text: "Female", checked: false},
        {id: "undefined", value: "undefined", text: "Who am I?", checked: false}
      ],
      dividerCreate: "remains",
      linkTitle: "Link",
      linkPlaceholder: "YouTube, Anilibria or file",
      createButton: "Create a room",
      dividerJoin: "or",
      codeTitle: "Room code",
      codePlaceholder: "BONK",
      joinButton: "Join"
    }
  },
  methods: {
    updateName(value) {
      this.localTextValue = value;
    },
    updateColor(value) {
      this.localColorValue = value;
    },
    updateSex(value) {
      this.localSexValue = value;
    },
    updateLink(value) {
      this.localLinkValue = value;
    },
    sendCreate() {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          {
            name: this.localTextValue,
            color: this.localColorValue,
            sex: this.localSexValue,
            link: this.localLinkValue
          }
        )
      };
      fetch("http://127.0.0.1:5000/room/create", requestOptions)
        .then(response => {
          if (response.status === 403) {
            this.$router.push({ name: "Index" });
            throw new Error("Error");
          }
          return response.json();
        })
        .then(data => {
          this.$router.push({ name: "Room", params: { roomId: data.room } });
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
  }

  .btn-create,
  .btn-join {
    width: 100%;
    margin-top: 1rem;
  }
}

@media screen and (max-width: 768px) {
  .form-title {
    line-height: 1;
    font-size: 1.275rem;
    margin-top: .5rem;
    margin-bottom: 1.5rem;
  }
}
</style>
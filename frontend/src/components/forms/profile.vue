<template>
  <form method="post" class="profile block">
    <div class="header">
      <h3 class="form-title">{{ $t("Profile") }}</h3>
    </div>
    <div class="form-inputs">
      <InputTextColor
          text-id="name"
          text-name="name"
          :text-value="nameValue"
          :text-storage="nameStorage"
          color-id="color"
          color-name="color"
          :color-value="colorValue"
          :color-storage="colorStorage"
          :placeholder='$t("Johnny Depp")'
          :label='$t("Name")'
          focus
          @textValueUpdated="updateName"
          @colorValueUpdated="updateColor"
      />
      <InputRadio
          classes="sexes"
          name="sex"
          :items="sexItems"
          :label='$t("Sex")'
          :storage="sexStorage"
          @radioValueUpdated="updateSex"
      />
      <InputRadio
          classes="languages"
          name="language"
          :items="languageItems"
          :label='$t("Language")'
          :storage="languageStorage"
          @radioValueUpdated="updateLanguage"
      />
      <button type="button" name="save" class="btn btn-primary btn-save" @click="saveProfile">
        {{ $t("Save") }}
      </button>
      <div class="home" v-if="$route.query.firstLogin !== 'true'">
        <Divider :text='$t("or")'/>
        <a href="/" class="btn btn-primary btn-home">
          {{ $t("Home") }}
        </a>
      </div>
    </div>
  </form>
</template>

<script>
import InputTextColor from "@/components/items/form/input-text-color";
import InputRadio from "@/components/items/form/input-radio";
import Divider from "@/components/items/form/divider";
import { nameStorage, colorStorage, sexStorage, languageStorage } from "@/storage";

export default {
  name: "FormComponent",
  components: {
    InputTextColor,
    InputRadio,
    Divider
  },
  data() {
    return {
      nameValue: "",
      colorValue: "#c76ad9",
      sexItems: [
        {id: "male", value: "male", text: "Male", checked: true},
        {id: "female", value: "female", text: "Female", checked: false},
        {id: "undefined", value: "undefined", text: "Who am I?", checked: false}
      ],
      languageItems: [
        {id: "en", value: "en", text: "English", checked: true},
        {id: "ru", value: "ru", text: "Russian", checked: false},
        {id: "ua", value: "ua", text: "Ukrainian", checked: false},
      ],
      nameStorage: nameStorage,
      colorStorage: colorStorage,
      sexStorage: sexStorage,
      languageStorage: languageStorage
    }
  },
  methods: {
    updateName(value) {
      this.localNameValue = value;
    },
    updateColor(value) {
      this.localColorValue = value;
    },
    updateSex(value) {
      this.localSexValue = value;
    },
    updateLanguage(value) {
      this.localLanguageValue = value;
    },
    saveProfile() {
      localStorage.setItem(this.nameStorage, this.localNameValue);
      localStorage.setItem(this.colorStorage, this.localColorValue);
      localStorage.setItem(this.sexStorage, this.localSexValue);
      localStorage.setItem(this.languageStorage, this.localLanguageValue);
      this.$i18n.locale = this.localLanguageValue;

      let room = this.$route.query.room;
      if (room) {
        this.$router.push({ name: "Room", params: { roomId: room } });
      } else {
        this.$router.push({ name: "Index" });
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.profile.block {
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

  .btn-home,
  .btn-save {
    width: 100%;
    margin-top: 1rem;
  }

  .btn-home {
    display: block;
    text-align: center;
    width: unset;
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
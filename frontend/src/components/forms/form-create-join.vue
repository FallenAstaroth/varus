<template>
  <form method="post" class="rooms block">
    <div class="header">
      <h3 class="form-title">{{ formTitle }}</h3>
    </div>
    <div class="form-inputs">
      <InputTextColor
          text-id="nick_text"
          text-name="name"
          text-value=""
          color-id="nick_color"
          color-name="nick_color"
          color-value="#c76ad9"
          :placeholder="namePlaceholder"
          :label="nameTitle"
      />
      <div class="label-input">
        <Label id="" :text="sexTitle"/>
        <div class="sexs">
          <InputRadio name="sex" id="male" value="male" :text="maleTitle"/>
          <InputRadio name="sex" id="female" value="female" :text="femaleTitle"/>
          <InputRadio name="sex" id="undefined" value="undefined" :text="undefinedTitle"/>
        </div>
      </div>
      <Divider :text="dividerCreate"/>
      <InputText
          id="links"
          name="links"
          value=""
          :placeholder="linkPlaceholder"
          :label="linkTitle"
      />
      <Button
          type="submit"
          name="create"
          class="btn-create"
          :text="createButton"
      />
      <Divider :text="dividerJoin"/>
      <InputText
          id="code"
          name="code"
          value=""
          :placeholder="codePlaceholder"
          :label="codeTitle"
      />
      <Button
          type="submit"
          name="join"
          class="btn-join"
          :text="joinButton"
      />
    </div>
  </form>
</template>

<script>
import InputText from "@/components/items/form/input-text";
import InputTextColor from "@/components/items/form/input-text-color";
import InputRadio from "@/components/items/form/input-radio";
import Label from "@/components/items/form/label";
import Divider from "@/components/items/form/divider";
import Button from "@/components/items/form/button";

export default {
  name: "FormComponent",
  components: {
    InputText,
    InputTextColor,
    InputRadio,
    Label,
    Divider,
    Button
  },
  data() {
    return {
      formTitle: "Varus TV",
      nameTitle: "Name",
      namePlaceholder: "Johnny Depp",
      sexTitle: "Sex",
      maleTitle: "Male",
      femaleTitle: "Female",
      undefinedTitle: "Who am I?",
      dividerCreate: "remains",
      linkTitle: "Link",
      linkPlaceholder: "YouTube or file",
      createButton: "Create a room",
      dividerJoin: "or",
      codeTitle: "Room code",
      codePlaceholder: "BONK",
      joinButton: "Join"
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/scss/items/form";

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

  .name-inputs {
    display: flex;
    gap: 10px;

    input[name="name"] {
      flex: 1;
    }
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
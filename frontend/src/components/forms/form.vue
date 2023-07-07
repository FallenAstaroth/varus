<template>
  <form method="post" class="rooms block">
    <div class="header">
      <h3 class="form-title">{{ formTitle }}</h3>
    </div>
    <div class="form-inputs">
      <div class="label-input">
        <Label id="nick_text" :text="nameTitle"/>
        <div class="name-inputs">
          <InputText :placeholder="namePlaceholder" name="name" id="nick_text" value=""/>
          <InputColor name="nick_color" id="nick_color" value="#c76ad9"/>
        </div>
      </div>
      <div class="label-input">
        <Label id="" :text="sexTitle"/>
        <div class="sexs">
          <InputRadio name="sex" id="male" value="male" :text="maleTitle"/>
          <InputRadio name="sex" id="female" value="female" :text="femaleTitle"/>
          <InputRadio name="sex" id="undefined" value="undefined" :text="undefinedTitle"/>
        </div>
      </div>
      <Divider :text="dividerCreate"/>
      <div class="label-input">
        <Label id="links" :text="linkTitle"/>
        <InputText :placeholder="linkPlaceholder" name="links" id="links" value=""/>
      </div>
      <Button type="submit" name="create" class="btn-create" :text="createButton"/>
      <Divider :text="dividerJoin"/>
      <div class="label-input join">
        <Label id="code" :text="codeTitle"/>
        <InputText :placeholder="codePlaceholder" name="code" id="code" value=""/>
      </div>
      <Button type="submit" name="join" class="btn-join" :text="joinButton"/>
    </div>
  </form>
</template>

<script>
import InputText from "@/components/items/form/input-text";
import InputRadio from "@/components/items/form/input-radio";
import InputColor from "@/components/items/form/input-color";
import Label from "@/components/items/form/label";
import Divider from "@/components/items/form/divider";
import Button from "@/components/items/form/button";

export default {
  name: "FormComponent",
  components: {
    InputText,
    InputRadio,
    InputColor,
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

<style lang="css">
.label-input {
  display: flex;
  flex-direction: column;
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

@media screen and (max-width: 768px) {
  .form-title {
    line-height: 1;
    font-size: 1.275rem;
    margin-top: .5rem;
    margin-bottom: 1.5rem;
  }

  .label-input {
    margin-top: .5rem;
  }
}
</style>
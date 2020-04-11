<template lang="html">
  <div id="firebaseui-auth-container"></div>
</template>

<script>
import firebase from "firebase/app";
import "firebase/auth";
import * as firebaseui from "firebaseui";
import { config } from "../helpers/firebaseConfig";
export default {
  name: "auth",
  mounted() {
    var uiConfig = {
      credentialHelper: firebaseui.auth.CredentialHelper.NONE,
      signInSuccessUrl: "/",
      signInOptions: [firebase.auth.EmailAuthProvider.PROVIDER_ID]
    };
    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start("#firebaseui-auth-container", uiConfig);
  }
};
</script>

<style lang="css"></style>

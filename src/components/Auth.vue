<template lang="html">
  <section>
    <!-- <div id="firebaseui-auth-container"></div> -->
    <b-field label="Gebruikersnaam">
      <b-input
        value=""
        v-model.trim="loginForm.email"
        @keyup.enter.native="login()"
      ></b-input>
    </b-field>
    <b-field label="Wachtwoord">
      <b-input
        value=""
        type="password"
        v-model.trim="loginForm.password"
        @keyup.enter.native="login()"
      ></b-input>
    </b-field>
    <b-field>
      <button class="button is-primary" @click="login()">Log in</button>
    </b-field>
  </section>
</template>

<script>
import firebase from "firebase/app";
import "firebase/auth";
// import * as firebaseui from "firebaseui";
import { config } from "../helpers/firebaseConfig";
export default {
  name: "auth",
  data() {
    return {
      loginForm: {
        email: "",
        password: ""
      }
    };
  },
  mounted() {
    // var uiConfig = {
    //   credentialHelper: firebaseui.auth.CredentialHelper.NONE,
    //   signInSuccessUrl: "/",
    //   signInOptions: [firebase.auth.EmailAuthProvider.PROVIDER_ID]
    // };
    // var ui = new firebaseui.auth.AuthUI(firebase.auth());
    // ui.start("#firebaseui-auth-container", uiConfig);
  },
  methods: {
    login() {
      const self = this;
      firebase
        .auth()
        .signInWithEmailAndPassword(
          self.loginForm.email,
          self.loginForm.password
        )
        .then(res => self.$router.push(`/`))
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style lang="css">
section {width: 400px; padding: 2rem;}
.button {font-family: 'Avenir LT W01 85 Heavy'; padding: 2rem}
</style>

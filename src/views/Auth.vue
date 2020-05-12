<template lang="html">
  <section>
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
import firebase from 'firebase/app';
import 'firebase/auth';
import { config } from '../helpers/firebaseConfig';
export default {
  name: 'auth',
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      }
    };
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
        .then(res => self.$router.push(`/places`))
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style lang="css" scoped>
section {width: 400px; padding: 2rem;}
.button {font-family: 'Avenir LT W01 85 Heavy'; margin:.4rem}
</style>

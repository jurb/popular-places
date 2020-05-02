import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Buefy from 'buefy';
import './assets/css/style.scss';
import '@mdi/font/css/materialdesignicons.css';
import firebase from 'firebase/app';
import 'firebase/auth';
import { config } from './helpers/firebaseConfig';

Vue.config.productionTip = true;

Vue.use(Buefy);

new Vue({
  router,
  created() {
    firebase.initializeApp(config);
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        this.$router.push('/places').catch(err => {});
      } else {
        this.$router.push('/auth').catch(err => {});
      }
    });
  },
  el: '#app',
  render: h => h(App)
});

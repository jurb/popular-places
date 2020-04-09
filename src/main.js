import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import App from "./App.vue";
import router from "./router";
import Buefy from "buefy";
import "./assets/css/style.scss";

Vue.config.productionTip = true;


Vue.use(VueAxios, axios);
Vue.use(Buefy);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");

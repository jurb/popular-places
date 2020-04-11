import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Auth from "./components/Auth.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    { path: "/auth", component: Auth }

    // ,
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: About
    // }
  ]
});

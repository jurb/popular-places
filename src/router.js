import Vue from 'vue';
import Router from 'vue-router';

const Home = () => import(/* webpackChunkName: "home" */ './views/Home.vue');
const Auth = () => import(/* webpackChunkName: "auth" */ './views/Auth.vue');

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/places',
      name: 'home',
      component: Home
    },
    { path: '/auth', component: Auth }

    // ,
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: About
    // }
  ]
});

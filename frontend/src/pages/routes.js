import { createRouter } from 'vue-router';

import Homepage from './home/home.vue';

// import SignIn from "./sign-in/SignIn.vue";
// import Cart from "./cart/Cart.vue";

const routes = [
  {
    path: "/",
    component: Homepage,
  },
];

export default function (history) {
  return createRouter({
    history,
    routes,
  });
}

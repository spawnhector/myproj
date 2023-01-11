// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";
// Import Quasar css
import "quasar/src/css/index.sass";
import "./style.css";
import "./style.scss";

import { createApp } from "vue";

import { createPinia } from "pinia";
import { AppFullscreen, Quasar } from "quasar";
import { createWebHistory } from "vue-router";

import App from "./App.vue";
import createRouter from "./lib/router.js";

const router = createRouter(createWebHistory());
const store = createPinia();
const myApp = createApp(App);
myApp
  .use(Quasar, {
    plugins: { AppFullscreen }, // import Quasar plugins and add here
  })
  .use(router)
  .use(store);
myApp.mount("#app");

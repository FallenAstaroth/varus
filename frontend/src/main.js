import { createApp } from "vue";
import VueCookies from 'vue3-cookies';
import App from "./App.vue";
import router from "./router";


const app = createApp(App);
app.use(VueCookies);
app.use(router);
app.mount("#app");

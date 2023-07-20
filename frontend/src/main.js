import {createApp} from "vue";
import VueCookies from "vue3-cookies";
import App from "@/App.vue";
import router from "@/router";
import i18n from "@/i18n";


const app = createApp(App);
app.use(VueCookies);
app.use(i18n);
app.use(router);
app.mount("#app");

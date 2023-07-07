import {createRouter, createWebHistory} from "vue-router";
import Index from "@/components/index.vue";


export default createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", component: Index }
    ]
})

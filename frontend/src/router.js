import {createRouter, createWebHistory} from "vue-router";
import Index from "@/components/index.vue";
import Room from "@/components/room.vue";


export default createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", component: Index },
        { path: "/room/:roomId", component: Room }
    ]
})

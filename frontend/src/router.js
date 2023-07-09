import {createRouter, createWebHistory} from "vue-router";
import Index from "@/components/index.vue";
import Room from "@/components/room.vue";
import Error from "@/components/404.vue";


export default createRouter({
    history: createWebHistory(),
    routes: [
        { name: "Index", path: "/", component: Index },
        { name: "Room", path: "/room/:roomId", component: Room },
        { name: "Error", path: "/:pathMatch(.*)", component: Error }
    ]
})

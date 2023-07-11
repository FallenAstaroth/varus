import { createRouter, createWebHistory } from "vue-router";
import Index from "@/components/index.vue";
import Room from "@/components/room.vue";
import Profile from "@/components/profile.vue";
import Error from "@/components/404.vue";
import { nameStorage, colorStorage, sexStorage } from "@/storage";


function requireProfile(to, from, next){
    let status = true;
    let storages = [nameStorage, colorStorage, sexStorage];
    storages.forEach(function(element) {
        if (!localStorage.getItem(element)) status = false;
    });
    if (status) {
        next();
    } else {
        const roomId = to.params.roomId;
        let url = "/profile?firstLogin=true";
        if (roomId) url += `&room=${roomId}`;
        next(url);
    }
}

export default createRouter({
    history: createWebHistory(),
    routes: [
        { name: "Index", path: "/", component: Index, beforeEnter: requireProfile },
        { name: "Room", path: "/room/:roomId", component: Room, beforeEnter: requireProfile },
        { name: "Profile", path: "/profile", component: Profile },
        { name: "Error", path: "/:pathMatch(.*)", component: Error }
    ]
})

import { createRouter, createWebHistory } from "vue-router";
import WelcomeView from "../views/WelcomeView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: WelcomeView,
    },
    {
      path: "/chattest",
      component: import("../components/ChatTest.vue") 
      // use this for all other pages (besides welcome page), for lazy-loading pages
    },
  ],
});

export default router;

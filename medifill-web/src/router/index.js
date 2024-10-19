import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';  // Correct component for home
import Questions from '../views/Questions.vue';  // Correct component for questions

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,  // Ensure this is the home page
    },
    {
      path: '/questions',
      name: 'questions',
      component: Questions,  // Ensure this is the questions page
    }
  ],
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
//import Login from '@/components/LoginPage.vue';
//import SignUp from '@/components/SignUpPage.vue';

const routes = [
  { path: '/', component: LandingPage },
  // { path: '/login', component: LandingPage },
  //{ path: '/signup', component: LandingPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
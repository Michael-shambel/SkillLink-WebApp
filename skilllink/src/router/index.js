// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import DashboardPage from '../components/DashboardPage.vue'; // Import the DashboardPage

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: RegisterPage },
  {
    path: '/dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true } // Add meta field to ensure only logged-in users can access this route
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Optional: Add navigation guard for authenticated routes
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('userToken'); // Check for user token on local storage
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    // If route requires authentication and user is not logged in, redirect to login
    next('/login');
  } else {
    next();
  }
});

export default router;

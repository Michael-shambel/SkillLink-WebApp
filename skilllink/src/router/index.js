/**
 * Set up routes for all pages in views
 */
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
//import LandingPage from '../views/LandingPage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import DashboardJobseeker from '../views/DashboardJobseeker.vue';
import DashboardEmployer from '../views/DashboardEmployer.vue';
import ProfileEmployer from '../views/ProfileEmployer.vue';
import ProfileJobseeker from '../views/ProfileJobseeker.vue'
import JobApplicants from '@/components/JobApplicants.vue';
import ApplicationDetails from '../components/ApplicationDetails.vue';
//import JobList from '../views/JobList.vue';

const routes = [
  { path: '/', component: HomePage },
  //{ path: '/', component: LandingPage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/dashboard/jobseeker', component: DashboardJobseeker },
  { path: '/dashboard/employer', component: DashboardEmployer },
  { path: '/profile/jobseeker', component: ProfileJobseeker },
  { path: '/profile/employer', component: ProfileEmployer },
  {
    path: '/dashboard/employer/job-posts/:job_post_id/applicants',
    component: JobApplicants,
  },
  {
    path: '/applications/:id',
    component: ApplicationDetails,
  }

  //{ path: '/jobs', component: JobList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

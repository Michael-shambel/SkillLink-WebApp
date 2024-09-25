<template>
    <AppNavbar />
  <div class="home">
    <!-- Hero Section -->
    <section class="hero text-center text-white d-flex align-items-center justify-content-center">
      <div class="container">
        <h1 class="display-4">Welcome to Skilllink</h1>
        <p class="lead">Connecting talented job seekers with top employers worldwide.</p>
        <div class="mt-4">
          <router-link to="/register" class="btn btn-primary btn-lg mx-2">Get Started as Job Seeker</router-link>
          <router-link to="/register" class="btn btn-outline-light btn-lg mx-2">Post a Job as Employer</router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features py-5 text-center">
      <div class="container">
        <h2 class="mb-4">Why Choose Skilllink?</h2>
        <div class="row">
          <div class="col-md-4">
            <i class="fas fa-briefcase fa-3x text-primary mb-3"></i>
            <h5>Job Matching</h5>
            <p>Find the perfect job that matches your skills and experience.</p>
          </div>
          <div class="col-md-4">
            <i class="fas fa-search fa-3x text-primary mb-3"></i>
            <h5>Skill-based Search</h5>
            <p>Easily search jobs by skills and location.</p>
          </div>
          <div class="col-md-4">
            <i class="fas fa-building fa-3x text-primary mb-3"></i>
            <h5>Top Companies</h5>
            <p>Connect with leading companies looking for talented professionals.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Job Search Section -->
    <section class="search-bar py-5">
      <div class="container">
        <form @submit.prevent="searchJobs">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="Search jobs by skills or location..." v-model="searchQuery" />
            <button class="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import apiClient from '../plugins/axios';
import AppNavbar from '../components/AppNavbar.vue';

export default {
data() {
  return {
    searchQuery: '',
    jobs: [], // Jobs fetched from Api
  };
},
methods: {
  async searchJobs() {
    try {
      const response = await apiClient.get(`/job-posts/?search=${this.searchQuery}`);
      this.jobs = response.data;
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  },
},
components: {
  AppNavbar,
},
};
</script>

<style scoped>
.hero {
height: 40vh;
/* background: url('../assets/background-image.jpg') no-repeat center center/cover; */
}
</style>
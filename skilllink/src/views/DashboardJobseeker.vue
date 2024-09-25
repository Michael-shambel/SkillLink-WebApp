<template>
    <div class="jobseeker-dashboard container">
      <NavbarDashboard userType='jobseeker'/>
  
      <h2 class="my-4 text-center">Job Seeker Dashboard</h2>
  
      <!-- Job-Search Section -->
      <div class="search-jobs mb-4">
        <form @submit.prevent="searchJobs">
          <div class="input-group">
            <input
              type="text"
              class="form-control"
              placeholder="Search jobs by skills or location"
              v-model="searchQuery"
            />
            <button class="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
      </div>
  
      <!-- Available Jobs Section -->
      <div class="available-jobs">
        <h3>Available Jobs</h3>
        <div v-if="jobs.length">
          <JobCard
            v-for="job in jobs"
            :key="job.id"
            :job="job"
            @apply="applyToJob"
          />
        </div>
        <div v-else>
          <p>No jobs found.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  /**
   * Fetch available jobs
   * Fetch jobs that the user has applied to
   * Search for jobs based on user input
   *  1. Get the token from local storage
   *  2. Send a GET request to the job-posts endpoint with the token in the headers
   * Apply to a job
   * If Authorization header(token) is missing/invalid throw a 401 error
   */
  import apiClient from '../plugins/axios';
  import NavbarDashboard from '../components/NavbarDashboard.vue';
  import JobCard from '../components/JobCard.vue';
  
  export default {
    data() {
      return {
        searchQuery: '',
        jobs: [], // List of available jobs
        appliedJobs: [], // List of jobs the user has applied to
      };
    },
    mounted() {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        this.$router.push('/login');
      } else {
        this.findJobs();
      }
    },
    computed: {
      token() {
        return localStorage.getItem('auth_token');
      },
    },
    methods: {
      async findJobs() {
        try {
          // const token = localStorage.getItem('auth_token');
          if (!this.token) {
            throw new Error("No token found. Please login");
          }
          const response = await apiClient.get(
            `/job-posts/?search=${this.searchQuery}`,
            {
              headers: {
                Authorization: `Token ${this.token}`,
              },
            }
          );
          this.jobs = response.data;
        } catch (error) {
          console.error('Error finding jobs:', error.response ? error.response.data : error.message);
        }
      },
      async applyToJob(jobId) {
        try {
          await apiClient.post(`/job-posts/${jobId}/apply/`, {}, {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          });
          alert('Successfully applied to job!');
        } catch (error) {
          console.error('Error applying to job:', error.response ? error.response.data : error.message);
        }
      },
    },
    components: {
      NavbarDashboard,
      JobCard,
    },
  };
  </script>
  
  <style scoped>
  .jobseeker-dashboard {
    max-width: 800px;
    margin: 0 auto;
  }
  </style>
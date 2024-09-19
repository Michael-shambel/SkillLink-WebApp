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
        <ul class="list-group">
          <li
            v-for="job in jobs"
            :key="job.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>{{ job.title }} - {{ job.location }}</span>
            <button class="btn btn-sm btn-primary" @click="applyToJob(job.id)">
              Apply
            </button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No jobs found.</p>
      </div>
    </div>

    <!-- Applied Jobs Section -->
    <div class="applied-jobs mt-5">
      <h3>Applied Jobs</h3>
      <ul class="list-group">
        <li
          v-for="application in appliedJobs"
          :key="application.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <span>{{ application.job_title }} - {{ application.status }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
/**
 * Fetch available jobs
 * Fetch jobs that the user has applied to
 * Search for jobs based on user input
 * Apply to a job
 */
import apiClient from '../plugins/axios';
import NavbarDashboard from '../components/NavbarDashboard.vue';

export default {
  data() {
    return {
      searchQuery: '',
      jobs: [], // List of available jobs
      appliedJobs: [], // List of jobs the user has applied to
    };
  },
  mounted() {
    this.fetchAvailableJobs();
    this.fetchAppliedJobs();
  },
  methods: {
    async fetchAvailableJobs() {
      try {
        const response = await apiClient.get('/job-posts/');
        this.jobs = response.data;
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    },
    async fetchAppliedJobs() {
      try {
        const response = await apiClient.get('/applications/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('auth_token')}`,
          },
        });
        this.appliedJobs = response.data;
      } catch (error) {
        console.error('Error fetching applied jobs:', error);
      }
    },
    async searchJobs() {
      try {
        const response = await apiClient.get(`/job-posts/?search=${this.searchQuery}`);
        this.jobs = response.data;
      } catch (error) {
        console.error('Error searching jobs:', error);
      }
    },
    async applyToJob(jobId) {
      try {
        await apiClient.post(`/job-posts/${jobId}/apply/`, {}, {
          headers: {
            Authorization: `Token ${localStorage.getItem('auth_token')}`,
          },
        });
        alert('Successfully applied to job!');
      } catch (error) {
        console.error('Error applying to job:', error);
      }
    },
  },
  components: {
    NavbarDashboard,
  },
};
</script>

<style scoped>
.jobseeker-dashboard {
  max-width: 800px;
  margin: 0 auto;
}
</style>
<template>
    <NavbarDashboard userType='employer' />
  <div class="employer-dashboard container">
    <h2 class="my-4 text-center">Employer Dashboard</h2>

    <!-- Create job post section-->
    <div class="create-job-post mb-4">
      <h3>Create Job Post</h3>
      <form @submit.prevent="createJobPost">
        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Job Title"
            v-model="jobTitle"
            required
          />
        </div>
        <div class="mb-3">
          <textarea
            class="form-control"
            placeholder="Job Description"
            v-model="jobDescription"
            required
          ></textarea>
        </div>
        <button class="btn btn-primary" type="submit">Create Job</button>
      </form>
    </div>

    <!-- Job posts section -->
    <div class="job-posts">
      <h3>Your Job Posts</h3>
      <ul class="list-group">
        <li
          v-for="job in jobPosts"
          :key="job.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <span>{{ job.title }} - {{ job.location }}</span>
          <button
            class="btn btn-sm btn-secondary"
            @click="viewApplicants(job.id)"
          >
            View Applicants
          </button>
        </li>
      </ul>
    </div>

    <!-- Search job seekers section -->
    <div class="search-jobseekers mt-5">
      <h3>Search Job Seekers</h3>
      <form @submit.prevent="searchJobseekers">
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Search by skills"
            v-model="searchQuery"
          />
          <button class="btn btn-primary" type="submit">Search</button>
        </div>
      </form>
      <ul v-if="jobseekers.length" class="list-group">
        <li
          v-for="jobseeker in jobseekers"
          :key="jobseeker.id"
          class="list-group-item"
        >
          {{ jobseeker.first_name }} {{ jobseeker.last_name }} - {{ jobseeker.skills }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
/**
 * Fetch jo posts for the employer
 * Create a new job post
 * View applicants for the job post
 * Search job seekers based on skills
 */
import apiClient from '../plugins/axios';
import NavbarDashboard from '../components/NavbarDashboard.vue';

export default {
  data() {
    return {
      jobTitle: '',
      jobDescription: '',
      jobPosts: [], // List of job posts
      jobseekers: [], // List of searched job seekers
      searchQuery: '',
    };
  },
  mounted() {
    this.fetchJobPosts();
  },
  methods: {
    async fetchJobPosts() {
      try {
        const response = await apiClient.get('/job-posts/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('auth_token')}`,
          },
        });
        this.jobPosts = response.data;
      } catch (error) {
        console.error('Error fetching job posts:', error);
      }
    },
    async createJobPost() {
      try {
        const response = await apiClient.post(
          '/job-posts/',
          {
            title: this.jobTitle,
            description: this.jobDescription,
            location: 'Remote', // You can extend to add location field
          },
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('auth_token')}`,
            },
          }
        );
        this.jobPosts.push(response.data);
        alert('Job created successfully!');
        this.jobTitle = '';
        this.jobDescription = '';
      } catch (error) {
        console.error('Error creating job post:', error);
      }
    },
    viewApplicants(jobId) {

      this.$router.push(`/job-posts/${jobId}/applicants`);
    },
    async searchJobseekers() {
      try {
        const response = await apiClient.get(
          `/search-jobseekers/?search=${this.searchQuery}`,
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('auth_token')}`,
            },
          }
        );
        this.jobseekers = response.data;
      } catch (error) {
        console.error('Error searching job seekers:', error);
      }
    },
  },
  components: {
    NavbarDashboard,
  },
};
</script>

<style scoped>
.employer-dashboard {
  max-width: 800px;
  margin: 0 auto;
}
</style>
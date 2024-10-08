<template>
  <NavbarDashboard userType='employer' />
  <div class="employer-dashboard container">
    <h2 class="my-4 text-center">Employer Dashboard</h2>

    <!-- Create job post section-->
    <div class="create-job-post mb-4">
      <h3>Create Job Post</h3>

      <div v-if="successMessage" class="alert alert-success" role="alert">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
      <form @submit.prevent="createJobPost">
        <div class="mb-3">
          <label for="title" class="form-label">Job Title</label>
          <input
            type="text"
            class="form-control"
            placeholder="Job Title"
            v-model="jobData.title"
            required
          />
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Job Description</label>
          <textarea
            class="form-control"
            placeholder="Job Description"
            v-model="jobData.description"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="skill" class="form-label">Skills</label>
          <input
            type="text"
            class="form-control"
            id="skills"
            v-model="jobData.skills_required"
            required
          />
        </div>

        <div class="mb-3">
          <label for="experience" class="form-label">Experience Required</label>
          <input
            type="text"
            class="form-control"
            id="experience"
            v-model="jobData.experience_required"
            required
          />
        </div>

        <div class="mb-3">
          <label for="location" class="form-label">Job Location</label>
          <input
            type="text"
            class="form-control"
            id="location"
            v-model="jobData.location"
            required
          />
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
          <!--On click viewApplicants job.id -->
          <router-link
            :to="`/dashboard/employer/job-posts/${job.id}/applicants`"
            class="btn btn-sm btn-secondary"
          >
            View Applicants
          </router-link>
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
* Create a new job post
* CreateJobPost method sends a POST request to /job-posts/ with the job data
*  1. Get the employer's token from localStorage
*  2. Make the POST request to the API to create a job post
*  3. On success, show a success message and reset form data
* View applicants for the job post
* Search job seekers based on skills
*/
import apiClient from '../plugins/axios';
import NavbarDashboard from '../components/NavbarDashboard.vue';

export default {
  data() {
    return {
      jobData: {
        title: '',
        description: '',
        skills_required: '',
        experience_required: '',
        location: '',
      },
      jobPosts: [], // List of job posts
      jobseekers: [], // List of searched job seekers
      searchQuery: '',
      successMessage: '',
      errorMessage: '',
    };
  },
  mounted() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.$router.push('/login');
    } else {
      this.fetchJobPosts();
    }
  },
  computed: {
    token() {
      return localStorage.getItem('auth_token');
    },
  },
  methods: {
    async fetchJobPosts() {
      try {
        const response = await apiClient.get('/job-posts/', {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.jobPosts = response.data;
      } catch (error) {
        console.error('Error fetching job posts:', error);
      }
    },
    async createJobPost() {
      try {
        if (!this.token) {
          throw new Error('No token found. Please login.');
        }

        await apiClient.post('/job-posts/', this.jobData, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });

        this.successMessage = 'Job post created successfully!';
        this.errorMessage = '';
        this.jobData = {
          title: '',
          description: '',
          skills_required: '',
          experience_required: '',
          location: '',
        };
      } catch (error) {
        console.error('Error creating job post:', error.response ? error.response.data : error.message);
        this.errorMessage = 'Error creating job post. Please try again';
      }
    },
    async searchJobseekers() {
      try {
        const response = await apiClient.get(
          `/search-jobseekers/?search=${this.searchQuery}`,
          {
            headers: {
              Authorization: `Token ${this.token}`,
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
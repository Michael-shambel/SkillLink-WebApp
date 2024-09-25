<template>
    <NavbarDashboard userType='employer' />
    <div class="container mt-4">
      <h3>Applicants for Job</h3>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <ul class="list-group">
        <li
          v-for="applicant in applicants"
          :key="applicant.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
            {{ applicant.applicant.email }} - Status: {{ applicant.status }}
  
          <!--Drop down to update status of each applicant-->
          <select v-model="applicant.status" @change="updateStatus(applicant)">
            <option value="pending">Pending</option>
            <option value="reviewed">Reviewed</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
          </select>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  /**
   * Initialize an empty list of applicants
   * Get the job ID from the URL
   * Get the auth_token
   * Fetch applicants when the fetchApplicants() is mounted
   * Create updateStatus method to update single applicant's status
   */
  import apiClient from '../plugins/axios';
  import NavbarDashboard from '../components/NavbarDashboard.vue';
  
  export default {
    data() {
      return {
        applicants: [],
        errorMessage: '',
      };
    },
    mounted() {
      this.fetchApplicants();
    },
    computed: {
      token() {
        return localStorage.getItem('auth_token');
      },
    },
    methods: {
      async fetchApplicants() {
        try {
          const jobId = this.$route.params.job_post_id;
          if (!this.token) {
            throw new Error("No token found. Please login");
          }
          // Fetch applicants for the job post
          const response = await apiClient.get(`/job-posts/${jobId}/applicants/`, {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          });
          this.applicants = response.data;
        } catch (error) {
          console.error('Error fetching applicants:', error.response ? error.response.data : error.message);
          this.errorMessage = 'Error fetching applicants. Please try again.';
        }
      },
  
      async updateStatus(applicant) {
        try {
          if (!this.token) {
            throw new Error("No token found. Please login");
          }
  
          // Send PATCH request to update the status
          await apiClient.patch(`/applications/${applicant.id}/`, {
            status: applicant.status,
          }, {
            headers: {
              Authorization: `Token ${this.token}`,
            },
          });
  
          alert('Application status updated successfully!');
          this.fetchApplicants(); // Refresh applicants list
        } catch (error) {
          this.errorMessage = 'Error updating status. Please try again.';
          console.error('Error updating status:', error);
        }
      },
    },
    components: {
      NavbarDashboard,
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 0 auto;
  }
  </style>
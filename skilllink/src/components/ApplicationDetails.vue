<template>
    <div class="container application-details mt-4">
      <h2>Application Details</h2>
  
      <div v-if="application">
        <h4>{{ application.job_title }}</h4>
        <p>Status: {{ application.status }}</p>
        <p>Applied on: {{ formatDate(application.applied_at) }}</p>
  
        <h5>Job Description</h5>
        <p>{{ application.job_description }}</p>
  
        <h5>Employer Details</h5>
        <p>{{ application.employer_name }}</p>
      </div>
  
      <div v-else>
        <p>Loading application details...</p>
      </div>
    </div>
  </template>
  
  <script>
  /**
   * application: Store application details
   * Get application ID from route params
   */
  import apiClient from '../plugins/axios';
  
  export default {
    data() {
      return {
        application: null,
      };
    },
    mounted() {
      this.fetchApplicationDetails();
    },
    methods: {
      async fetchApplicationDetails() {
        const applicationId = this.$route.params.id;
        const response = await apiClient.get(`/applications/${applicationId}/`);
        this.application = response.data;
      },
      formatDate(date) {
        return new Date(date).toLocaleDateString();
      },
    },
  };
  </script>
  
  <style scoped>
  .application-details {
    max-width: 800px;
    margin: 0 auto;
  }
  </style>
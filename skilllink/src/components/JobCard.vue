<template>
    <div class="job-card p-3 mb-4 shadow-sm border rounded">
      <!-- Posted time & location row -->
      <div class="d-flex justify-content-between align-items-start mb-2">
        <small class="text-muted">{{ formatDate(job.posted_on) }}</small>
        <span class="text-muted">
          <i class="bi bi-geo-alt"></i> {{ job.location }}
        </span>
      </div>
  
      <!-- Job title & price -->
      <div class="job-header mb-2">
        <h5 class="fw-bold">{{ job.title }}</h5>
        <p class="text-primary">{{ formatPrice(job.price) }}</p>
      </div>
  
      <!-- Job description -->
      <div class="job-description mb-3">
        <p>{{ job.description }}</p>
      </div>
  
      <!-- Skills, Applicants & experience -->
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <i class="bi bi-person"></i>
          <small>{{ job.applications_count }} Applicants</small>
        </div>
        <div class="text-center">
          <small class="fw-light">Skills: {{ job.skills_required }}</small>
        </div>
        <div>
          <small>Experience: {{ job.experience_required }}</small>
        </div>
      </div>
  
      <div class="d-flex justify-content-end mt-3">
        <button @click="applyToJob(job.id)" class="btn btn-success">Apply</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ["job"],
    methods: {
      formatDate(date) {
        return new Date(date).toLocaleDateString();
      },
      formatPrice(price) {
        return price ? `$${price}` : "Fixed";
      },
      applyToJob(jobId) {
        this.$emit('apply', jobId);
      }
    },
  };
  </script>
  
  <style scoped>
  .job-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
  }
  .job-header h5 {
    font-size: 1.25rem;
  }
  .job-description p {
    margin: 0;
    color: #6c757d;
  }
  .job-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
  }
  
  </style>
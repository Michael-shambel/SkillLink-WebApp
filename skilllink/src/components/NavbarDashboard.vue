<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">SkillLink</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item dropdown">
            <button
              class="nav-link dropdown-toggle"
              id="appliedJobsDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              @click.prevent="toggleDropDown"
            >
              Applied Jobs
          </button>
            <ul class="dropdown-menu" aria-labelledby="appliedJobsDropdown">
              <li
                v-for="application in appliedJobs"
                :key="application.id"
                class="dropdown-item"
                @click="showJobDetails(application)"
              >
                {{ application.job_title }} - {{ application.status }}
              </li>
              <li v-if="!appliedJobs.length" class="dropdown-item text-muted">
                No applied jobs yet.
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <router-link :to="profileLink" class="nav-link">
              <img
                :src="profileIcon"
                alt="Profile"
                class="rounded-circle"
                width="30"
                height="30"
              />
              Profile
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="#" class="nav-link">
              <i class="fas fa-envelope"></i> Messages
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="#" class="nav-link">
              <i class="fas fa-credit-card"></i> Billing
            </router-link>
          </li>
          <li class="nav-item">
            <button class="btn nav-link" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- A draggable pop-up Job Details Panel -->
  <div :class="['job-details-panel', { 'panel-open': panelOpen }]">
    <div class="panel-header">
      <button class="btn btn-secondary" @click="closeJobDetails">
        <i class="bi bi-arrow-left"></i> Back
      </button>
      <h4>{{ selectedJob.job_title }}</h4>
    </div>
    <div class="panel-body">
      <p>Status: {{ selectedJob.status }}</p>
      <p>Applied on: {{ formatDate(selectedJob.applied_at) }}</p>
      <h5>Job Description</h5>
      <p>{{ selectedJob.job_description }}</p>
      <h5>Employer Details</h5>
      <p>{{ selectedJob.employer_name }}</p>
    </div>
  </div>
</template>

<script>
/**
 * Uses default user photo
 * Dynamically link correct profile page based on user type
 * Clears the token on local strorage and redirects the user to the login page
 * Fetch the list of applied jobs from the API
 */
 import apiClient from '../plugins/axios';

export default {
  props: ['userType'],
  data() {
    return {
      appliedJobs: [],
      selectedJob: {},
      panelOpen: false,
      dropdownOpen: false,
      profileIcon: require('@/assets/default-profile.jpeg'),
    };
  },
  computed: {
    profileLink() {
      return this.userType === 'employer' ? '/profile/employer' : '/profile/jobseeker';
    },
  },
  mounted() {
    this.fetchAppliedJobs();
  },
  methods: {
    async fetchAppliedJobs() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          throw new Error("No token found. Please login");
        }
        const response = await apiClient.get('/applications/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.appliedJobs = response.data;
      } catch (error) {
        console.error('Error fetching applied jobs:', error.response ? error.response.data : error.message);
      }
    },
    showJobDetails(application) {
      this.selectedJob = application;
      this.panelOpen = true;
    },
    closeJobDetails() {
      this.panelOpen = false;
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    logout() {
      localStorage.removeItem('auth_token');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  /*background: rgba(87, 174, 175, 0.9);*/
}
.navbar .nav-link img {
  margin-right: 8px;
}
.navbar .nav-link i {
  margin-right: 5px;
}
.navbar-brand {
  padding-right: 10px;
}
.navbar-nav {
  padding-left: 10px;
}

.job-details-panel {
  position: fixed;
  top: 0;
  right: -70%;
  width: 70%;
  height: 100%;
  background-color: white;
  box-shadow: -4px 0 8px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 1050; /* Above the content */
  overflow-y: auto;
}
.job-details-panel.panel-open {
  right: 0;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}
.panel-body {
  padding: 1rem;
}
.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
<template>
  <div>
    <!-- Top Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Dashboard Menu Icon -->
        <div class="navbar-brand">
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              id="dashboardDropdown"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Dashboard
            </button>
            <ul class="dropdown-menu" aria-labelledby="dashboardDropdown">
              <li><a class="dropdown-item" href="#">Calendar</a></li>
              <li><a class="dropdown-item" href="#">Rating & Review</a></li>
              <li><a class="dropdown-item" href="#">Log Out</a></li>
            </ul>
          </div>
        </div>

        <!-- Navbar Links -->
        <div class="collapse navbar-collapse justify-content-between">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#">Job Posting</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Messages</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Billing</a>
            </li>
          </ul>

          <!-- Profile Icon with Name -->
          <div class="d-flex align-items-center">
            <img
              :src="profilePicture"
              class="rounded-circle"
              width="40"
              height="40"
              alt="Profile Picture"
            />
            <div class="ms-2">
              <a class="nav-link" href="#">Profile</a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Job Search Bar -->
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="input-group">
            <input
              type="text"
              class="form-control"
              placeholder="Job Title"
              v-model="jobTitle"
            />
            <input
              type="text"
              class="form-control"
              placeholder="Location"
              v-model="location"
            />
            <button class="btn btn-primary" @click="searchJobs">Search</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer mt-auto py-3 bg-dark text-light">
      <div class="container text-center">
        <p>&copy; {{ new Date().getFullYear() }} SkillLink. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  data() {
    return {
      profilePicture: '', // Profile picture URL or empty string
      jobTitle: '',
      location: '',
    };
  },
  methods: {
    searchJobs() {
      // Logic for job search goes here
      console.log('Searching for:', this.jobTitle, this.location);
    },
  },
  mounted() {
    // Set a default profile picture if none is uploaded
    this.profilePicture =
      this.profilePicture || 'https://via.placeholder.com/150'; // Placeholder image URL
  },
};
</script>

<style scoped>
.navbar-brand .dropdown-toggle {
  background-color: #007bff;
  color: white;
}

.navbar-brand .dropdown-toggle:hover {
  background-color: #0056b3;
}

.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.input-group {
  margin-top: 50px;
}

.footer {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}
</style>

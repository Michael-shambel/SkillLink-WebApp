<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <div class="container">
      <router-link to="/" class="navbar-brand">Skilllink</router-link>

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
</template>

<script>
/**
 * Uses default user photo
 * Dynamically link correct profile page based on user type
 * Clears the token on local strorage and redirects the user to the login page
 */
export default {
  props: ['userType'],
  data() {
    return {
      profileIcon: require('@/assets/default-profile.jpeg'),
    };
  },
  computed: {
    profileLink() {
      return this.userType === 'employer' ? '/profile/employer' : '/profile/jobseeker';
    },
  },
  methods: {
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
</style>
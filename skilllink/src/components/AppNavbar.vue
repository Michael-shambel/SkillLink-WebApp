<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand ms-2" to="/">SkillLink</router-link>
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
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav ms-auto text-end">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/signup">Sign Up</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </template>

  <script>
  export default {
    name: "AppNavbar",
  };
  </script>

  <style scoped>
  .navbar-brand {
    font-weight: bold;
  }
  </style>
<template>
    <footer class="bg-dark text-white text-center py-2">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} Skilllink. All rights reserved.</p>
        <div>
          <a href="#" class="text-white me-3">
            <i class="fab fa-facebook"></i>
          </a>
          <a href="#" class="text-white me-3">
            <i class="fab fa-twitter"></i>
          </a>
          <a href="#" class="text-white">
            <i class="fab fa-linkedin"></i>
          </a>
        </div>
      </div>
    </footer>
  </template>

  <script>
  export default {};
  </script>

  <style scoped>
  footer {
    background-color: #343a40;
  }
  footer a {
    color: #fff;
  }
  </style>
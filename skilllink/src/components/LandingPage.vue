<template>
    <div class="welcome-section">
      <div class="section-box">
        <h1>Welcome to SkillLink</h1>
        <p class="lead">Search through thousands of job opportunities or skilled professionals near you.</p>
      </div>
    </div>

    <!--Footer section-->
    <footer class="footer mt-auto py-3 bg-dark text-light">
    <div class="container text-center">
      <p>&copy; {{ new Date().getFullYear() }} SkillLink. All rights reserved.</p>
      <ul class="list-inline">
        <li class="list-inline-item">
          <router-link class="text-light" to="/about">About Us</router-link>
        </li>
        <li class="list-inline-item">
          <router-link class="text-light" to="/privacy">Privacy Policy</router-link>
        </li>
        <li class="list-inline-item">
          <router-link class="text-light" to="/terms">Terms of Service</router-link>
        </li>
      </ul>
      <div class="social-icons mt-2">
        <a href="#" class="text-light me-2"><i class="fab fa-facebook"></i></a>
        <a href="#" class="text-light me-2"><i class="fab fa-twitter"></i></a>
        <a href="#" class="text-light"><i class="fab fa-linkedin"></i></a>
        <a href="#" class="text-light"><i class="fab fa-whatsup"></i></a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "LandingPage",
};
</script>

<style scoped>
.welcome-section {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
  height: 100vh;
  background: linear-gradient(to top, #013220, rgba(1, 50, 32, 0.1));
  color: white;
}

.section-box {
  background-color: #f1f1f1;
  padding: 60px;
  border-radius: 30px;
  box-shadow: 0px, 4px, 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.section-box h1 {
  font-size: 3rem;
  color: #008080;
  font-weight: bold;
}

.section-box p.lead {
  font-size: 1.25rem;
  margin-top: 20px;
  color: #6c757d;
}

@media (max-width: 768px) {
  .section-box {
    padding: 30px;
  }

  .section-box h1 {
    font-size: 2.5rem;
  }

  .section-box p.lead {
    font-size: 1.1rem;
  }
}
</style>

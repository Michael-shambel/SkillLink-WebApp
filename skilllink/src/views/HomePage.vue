<template>
  <AppNavbar />

  <!-- Welcome Section -->
  <section id="home-page" class="home-page full-height d-flex align-items-center justify-content-center">
    <div class="container text-center p-0">
      <div class="welcome-section">
        <h1 class="display-3">Welcome to SkillLink</h1>
        <p class="lead">Connecting talented job seekers with top employers worldwide.</p>
        <div class="mt-4">
          <router-link to="/register" class="btn btn-primary btn-lg mx-2">Get Started as Job Seeker</router-link>
          <router-link to="/register" class="btn btn-outline-dark btn-lg mx-2">Post a Job as Employer</router-link>
        </div>
      </div>
    </div>
  </section>

  <!-- About Section -->
  <section id="about-section" class="about-section py-5 text-center">
    <div class="container-fluid p-0">
      <h2 class="mb-4">Why Choose SkillLink?</h2>
      <div class="row mx-0">
        <div class="col-md-4">
          <i class="fas fa-briefcase fa-3x text-dark mb-3"></i>
          <h5>Job Matching</h5>
          <p>Find the perfect job that matches your skills and experience.</p>
        </div>
        <div class="col-md-4">
          <i class="fas fa-search fa-3x text-dark mb-3"></i>
          <h5>Skill-based Search</h5>
          <p>Easily search jobs by skills and location.</p>
        </div>
        <div class="col-md-4">
          <i class="fas fa-handshake fa-3x text-dark mb-3"></i>
          <h5>Potential Employer</h5>
          <p>Connect with potential employers looking for skilled, talented professionals.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Contact Section -->
  <section id="contact" class="contact-section py-5 text-center">
    <div class="container-fluid p-0">
      <h2 class="mb-4">Have Any Questions?</h2>
      <p>Contact us by filling in the form below</p>

      <form class="text-center w-50 mx-auto">
        <div class="form-group mb-3">
          <input type="email" class="form-control" placeholder="Enter your email" />
        </div>
        <div class="form-group mb-3">
          <textarea class="form-control" placeholder="Enter your message" rows="5"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Send Message</button>
      </form>
    </div>
  </section>
</template>

<script>
import AppNavbar from '../components/AppNavbar.vue';

export default {
  components: {
    AppNavbar,
  },
};
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow-x: hidden;
  background-color: white;
  color: black;
}

.home-page,
.about-section,
.contact-section {
  width: 100%;
  margin: 0;
  padding: 0;
  color: black;
}

.welcome-section {
  margin-top: 20px;
  margin-bottom: 40px;
}

.about-section, .contact-section {
  padding-top: 60px;
  padding-bottom: 60px;
  background-color: white;
}

.contact-section {
  background-color: #495057;
}

form .form-control {
  border-radius: 5px;
}

form button {
  width: 100%;
}
</style>
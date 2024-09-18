<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="row w-100 justify-content-center">
      <div class="col-md-6 col-lg-4">
        <h2 class="text-center mb-4">Sign Up</h2>
        <form @submit.prevent="registerUser">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" v-model="email" class="form-control" id="email" required />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" v-model="email" class="form-control" id="email" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" v-model="password" class="form-control" id="password" required />
          </div>
          <div class="mb-3">
            <label for="is_jobseeker" class="form-label">Are you a Job Seeker?</label>
            <input type="checkbox" v-model="is_jobseeker" />
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Sign Up</button>
          </div>
          <p class="text-center mt-3">
            Already have an account? <router-link to="/login">Login here</router-link>.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

  <script>
  import axios from 'axios';

  export default {
    name: 'RegisterPage',
    data() {
      return {
        email: '',
        password: '',
        is_jobseeker: false
      };
    },
    methods: {
      registerUser() {
        axios.post('http://127.0.0.1:8000/api/register/', {
          email: this.email,
          password: this.password,
          is_jobseeker: this.is_jobseeker
        })
        .then(response => {
          // Store the token and redirect after successful registration
          localStorage.setItem('userToken', response.data.token);
          this.$router.push('/'); // Redirect to home/landing page
        })
        .catch(error => {
          console.error('Registration failed', error);
          alert('Registration failed. Please try again.');
        });
      }
    }
  };
  </script>

<style scoped>
.min-vh-100 {
  min-height: 100vh;
}
</style>
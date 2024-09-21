<template>
    <div class="login-page container">
      <h2 class="text-center my-4">Login to Skilllink</h2>

      <!-- Success Alert -->
      <div v-if="successMessage" class="alert alert-success" role="alert">
        {{ successMessage }}
      </div>

      <!-- Error Alert -->
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
    </div>
</template>

<script>
import apiClient from '../plugins/axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await apiClient.post('/token/', {
          email: this.email,
          password: this.password,
        });

        this.successMessage = 'Login successful!';
        this.errorMessage = '';

        const token = response.data.token;
        const userData = response.data.user;

        if (!token) {
        throw new Error('Token not found in response');
        }

        // Store the token in localStorage
        localStorage.setItem('auth_token', token);

        // Check if userData exists and redirect based on user type
        if (userData) {
          if (userData.is_employer) {
            this.$router.push('/dashboard/employer');
          } else if (userData.is_jobseeker) {
            this.$router.push('/dashboard/jobseeker');
          } else {
            this.errorMessage = 'Unknown user type';
          }
        } else {
          this.errorMessage = 'Invalid user data';
        }
      } catch (error) {
        // Log the error to the console for debugging
        console.error('Login error:', error.response ? error.response.data : error.message);
        this.errorMessage = 'Invalid email or password';
        this.successMessage = '';
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
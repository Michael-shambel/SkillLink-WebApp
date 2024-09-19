<template>
    <div class="register-page container">
      <h2 class="text-center my-4">Register for Skilllink</h2>

      <!-- Success Alert -->
      <div v-if="successMessage" class="alert alert-success" role="alert">
        {{ successMessage }}
      </div>

      <!-- Error Alert -->
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="register">
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
        <div class="mb-3">
          <label class="form-label">I am a:</label>
          <select v-model="userType" class="form-select" required>
            <option value="jobseeker">Job Seeker</option>
            <option value="employer">Employer</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary w-100">Register</button>
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
      userType: 'jobseeker',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async register() {
      try {
        const isJobSeeker = this.userType === 'jobseeker';

        const response = await apiClient.post('/register/', {
          email: this.email,
          password: this.password,
          is_jobseeker: isJobSeeker,
          is_employer: !isJobSeeker,
        });

        this.successMessage = 'Registration successful!';
        this.errorMessage = '';

        localStorage.setItem('auth_token', response.data.token);

        // Redirect based on user type
        if (isJobSeeker) {
          this.$router.push('/dashboard/jobseeker');
        } else {
          this.$router.push('/dashboard/employer');
        }
      } catch (error) {
        this.errorMessage = 'Registration failed. Please try again.';
        this.successMessage = '';
      }
    },
  },
};
</script>

<style scoped>
  .register-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
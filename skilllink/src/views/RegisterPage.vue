<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">SkillLink</router-link>
    </div>
  </nav>
  <div class="register-page my-4">
    <h2 class="text-center">Register for Skilllink</h2>

    <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
    <div v-if="errorMessage" class="alert alert-danger" role="alert">{{ errorMessage }}</div>

    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          :class="{ 'is-invalid': emailError }"
          @input="validateEmail"
          required
        />
        <div v-if="emailError" class="invalid-feedback">{{ emailError }}</div>
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          placeholder="Password (6 or more characters)"
          v-model="password"
          class="form-control"
          :class="{ 'is-invalid': passwordError }"
          @input="validatePassword"
          required
        />
        <div v-if="passwordError" class="invalid-feedback">{{ passwordError }}</div>
      </div>
      <div class="mb-3">
        <label class="form-label">I am a:</label>
        <select v-model="userType" class="form-select" required>
          <option value="jobseeker">Job Seeker</option>
          <option value="employer">Employer</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary w-100">Register</button>
      <p class="text-center mt-3">
        Already have an account? <router-link to="/login">Login here</router-link>.
      </p>
    </form>

    <hr />

    <div class="google-signup">
      <p class="text-center">Or Register with Google</p>
      <button
        class="btn btn-danger"
        @click="googleSignUp"
        id="google-signin-btn"
      >
        <i class="fab fa-google"></i> Sign up with Google
      </button>
    </div>
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
      userType: 'jobseeker',
      emailError: '',
      passwordError: '',
    };
  },
  mounted() {
    if (!this.$gAuth) {
      console.error("Google Sign-In is not initialized or $gAuth is undefined");
    } else {
      console.log("Google Sign-In initialized successfully");
      this.googleSignUp();
    }
  }, 
  methods: {
    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.emailError = 'Email is required';
      } else if (!emailPattern.test(this.email)) {
        this.emailError = 'Please enter a valid email address';
      } else {
        this.emailError = '';
      }
    },
    validatePassword() {
      if (!this.password) {
        this.passwordError = 'Password is required';
      } else if (this.password.length < 6) {
        this.passwordError = 'Password must be at least 6 characters';
      } else {
        this.passwordError = '';
      }
    },
    async register() {
      this.validateEmail();
      this.validatePassword();
      if (this.emailError || this.passwordError) {
        return;
      }

      try {
        const isJobSeeker = this.userType === 'jobseeker';
        const response = await apiClient.post('/register/', {
          email: this.email,
          password: this.password,
          is_jobseeker: isJobSeeker,
          is_employer: !isJobSeeker,
        });

        if (response.data.message) {
          this.successMessage = 'Registration successful!';
          this.errorMessage = '';

          localStorage.setItem('auth_token', response.data.token);

          this.$router.push('/login');
        }
      } catch (error) {
        this.errorMessage = 'Registration failed. Please try again.';
        this.successMessage = '';
      }
    },
    async googleSignUp() {
      try {
        const googleUser = await this.$gAuth.signIn();
        const idToken = googleUser.getAuthResponse().id_token;

        const isJobSeeker = this.userType === 'jobseeker';
        const response = await apiClient.post('/register/', {
          google_token: idToken,
          is_jobseeker: isJobSeeker,
          is_employer: !isJobSeeker,
        });

        if (response.data.success) {
          this.successMessage = 'Registration successful!';
          this.errorMessage = '';

          localStorage.setItem('auth_token', response.data.token);

          this.$router.push('/login');
        } else {
          this.errorMessage = 'Registration failed. User already exists.';
        }
      } catch (error) {
        console.error('Google Sign-Up Error:', error);
        this.errorMessage = 'Google Sign-Up failed. Please try again.';
      }
    },
  },
};
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 80px auto;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); /* Soft shadow effect */
  transition: all 0.3s ease-out-in;
}

.google-signup {
  text-align: center;
  margin-top: 20px;
}

.register-page:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

button {
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  width: 100%;
}

button:hover {
  background-color: #0056b3;
}

.invalid-feedback {
  color: red;
  font-size: 0.875em;
}

.is-invalid {
  border-color: red;
}

.btn-google {
  background-color: #db4437;
  color: white;
  border: none;
}

.btn-google:hover {
  background-color: #c33d2e;
}
</style>
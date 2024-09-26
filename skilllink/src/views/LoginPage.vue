<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Skilllink</router-link>
    </div>
  </nav>
  <div class="login-page my-4">
    <h2 class="text-center">Login to Skilllink</h2>

    <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
    <div v-if="errorMessage" class="alert alert-danger" role="alert">{{ errorMessage }}</div>

    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          :class="{ 'is-invalid': emailError }"
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
          required
        />
        <div v-if="passwordError" class="invalid-feedback">{{ passwordError }}</div>
      </div>

      <button type="button" @click="googleSignIn" class="btn btn-outline-primary w-100 mb-3">
        Sign in with Google
      </button>
      <button type="submit" class="btn btn-primary w-100">Login</button> <!--:disabled="emailError || passwordError"-->

      <p class="text-center mt-3">
        Don't have an account? <router-link to="/register">Register here</router-link>.
      </p>
    </form>
  </div>
</template>

<script>
/**
 * Frontend sends google_token request and handle_google_login method is invoked in the backend
 * The method verifies the token using Google OAuth2 API
 * googleUser.getAuthResponse(): this function is part of google API libraries
 * it returns an object containing info about the user's authentication session
 * - GOOGLE_ID_TOKEN - ACCESS_TOKEN - Expiration times - scope - token type
 * id_token: this is the GOOGLE_ID_TOKEN. contains users details like name, email, etc. Used for
 * simple authentication 
 * Access token: used to access Google APIs (like Google Drive or Google Calendar)
 * If valid, it fetches a user based on their email or creates a new user
*/
import apiClient from '../plugins/axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      successMessage: '',
      errorMessage: '',
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
    async login() {
      this.validateEmail();
      this.validatePassword();

      if (this.emailError || this.passwordError) {
        return;
      }
      try {
        const { data } = await apiClient.post('/token/', { email: this.email, password: this.password });
        const { token, user } = data;

        if (!token) throw new Error('Token not found in response');

        localStorage.setItem('auth_token', token);

        // Check user type and redirect to their respective dashboards
        if (user.is_jobseeker) {
          this.$router.push('/dashboard/jobseeker');
        } else {
          this.$router.push('/dashboard/employer');
        }

        this.successMessage = 'Login successful!';
        this.errorMessage = '';

      } catch (error) {
        this.errorMessage = 'Invalid email or password';
        this.successMessage = '';
      } 
    },
    async googleSignIn() {
      try {
        const googleUser = await this.$gAuth.signIn();
        const idToken = googleUser.getAuthResponse().id_token;
        const data = await apiClient.post('/token/', { google_token: idToken });

        console.log("Google ID Token: ", idToken);
        console.log('Authenticated User:', data);
      } catch (error) {
        console.error("Google Sign-In error: ", error);
        this.errorMessage = 'Google sign-in failed';
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  max-width: 400px;
  margin: 100px auto;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); /* Soft shadow effect */
  transition: all 0.3s ease-in-out;
}

.login-page:hover {
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
</style>
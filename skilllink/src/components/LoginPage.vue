<template>
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="row w-100 justify-content-center">
        <div class="col-md-6 col-lg-4">
          <h2 class="text-center mb-4">Login</h2>
          <form @submit.prevent="loginUser">
            <div class="mb-3">
              <label for="email" class="form-label">Email address</label>
              <input type="email" v-model="email" class="form-control" id="email" required />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" v-model="password" class="form-control" id="password" required />
            </div>
            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Login</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'LoginPage',
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      loginUser() {
        // Example of using axios to log in
        axios
          .post('http://127.0.0.1:8000/api/token/', {
            email: this.email,
            password: this.password
          })
          .then((response) => {
            // Store token in localStorage or Vuex
            localStorage.setItem('userToken', response.data.token);
  
            // Redirect to the dashboard after successful login
            this.$router.push('/dashboard');
          })
          .catch((error) => {
            console.error('Login failed:', error);
            alert('Invalid credentials. Please try again.');
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
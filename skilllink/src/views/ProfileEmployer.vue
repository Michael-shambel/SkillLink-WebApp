<template>
  <div class="employer-profile container">
    <h2 class="my-4 text-center">Create Your Employer Profile</h2>

    <!-- Success Alert -->
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <!-- Error Alert -->
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="submitProfile">
      <div class="mb-3">
        <label for="first_name" class="form-label">First Name</label>
        <input
          type="text"
          class="form-control"
          id="first_name"
          v-model="firstName"
          required
        />
      </div>
      <div class="mb-3">
        <label for="last_name" class="form-label">Last Name</label>
        <input
          type="text"
          class="form-control"
          id="last_name"
          v-model="lastName"
          required
        />
      </div>
      <div class="mb-3">
        <label for="location" class="form-label">Location</label>
        <input
          type="text"
          class="form-control"
          id="location"
          v-model="location"
          required
        />
      </div>
      <div class="mb-3">
        <label for="phone_number" class="form-label">Phone Number</label>
        <input
          type="tel"
          class="form-control"
          id="phone_number"
          v-model="phoneNumber"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary w-100">Save Profile</button>
    </form>
  </div>
</template>

<script>
/**
 * Fields: Firstname, Lastname, location, phonenumber
 * A POST request is made to the /employers/ endpoint to create/update the profile
 */
import apiClient from '../plugins/axios';

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      location: '',
      phoneNumber: '',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async submitProfile() {
      try {
        await apiClient.post(
          '/employers/',
          {
            first_name: this.firstName,
            last_name: this.lastName,
            location: this.location,
            phone_number: this.phoneNumber,
          },
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('auth_token')}`,
            },
          }
        );

        this.successMessage = 'Profile created successfully!';
        this.errorMessage = '';
      } catch (error) {
        console.error('Error details:', error.response ? error.response.data : error.message);
        this.errorMessage = 'Error creating profile. Please try again.';
        this.successMessage = '';
      }
    },
  },
};
</script>

<style scoped>
.employer-profile {
  max-width: 600px;
  margin: 0 auto;
}
</style>
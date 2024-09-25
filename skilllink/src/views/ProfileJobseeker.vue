<template>
  <div class="jobseeker-profile container">
    <h2 class="my-4 text-center">Create Your Job Seeker Profile</h2>

    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

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
        <label for="skills" class="form-label">Skills</label>
        <input
          type="text"
          class="form-control"
          id="skills"
          v-model="skills"
          placeholder="e.g. Python, Django, REST APIs"
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
 * Fields: First name, Last name, skills, Phonenumber
 * A POST request is made to the /jobseekers/ endpoint to create or update the profile
 */
import apiClient from '../plugins/axios';

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      skills: '',
      phoneNumber: '',
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async submitProfile() {
      try {
        await apiClient.post(
          '/jobseekers/',
          {
            first_name: this.firstName,
            last_name: this.lastName,
            skills: this.skills,
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
.jobseeker-profile {
  max-width: 600px;
  margin: 0 auto;
}
</style>
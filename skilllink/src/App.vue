<template>
  <div id="app">
    <AppNavbar />

    <!-- This will render the routed pages -->
    <router-view></router-view>
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue'

export default {
  name: 'App',
  components: {
    AppNavbar,
  },
};
</script>

<style>
  /*Global styles will apply here*/
</style>

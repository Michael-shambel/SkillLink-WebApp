<template>
  <div id="app">

    <main class="container my-5">
      <router-view></router-view>
    </main>

    <FooterBlock />
  </div>
</template>

<script>
import FooterBlock from './components/FooterBlock.vue';

export default {
  components: {
    FooterBlock,
  },
};
</script>

<style>
body {
  font-family: 'Arial', sans-serif;
  background-color: #d6e8fa;
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

@media (max-width: 576px) {
  main {
    padding: 0 1rem;
  }
}
</style>
<template>
  <div id="app">

    <main class="container my-5">
      <router-view/>
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

<style scoped>
body {
  font-family: 'Arial', sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
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
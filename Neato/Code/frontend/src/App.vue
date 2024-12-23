<template>
  <div id="app">
    <NavBar />
    <router-view></router-view>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  margin: 0px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* Background image styles */
  background-image: url('../src/assets/new.jpg');
  background-size: cover;
  background-position: top;
  background-repeat: no-repeat;


  html,
  body {
    margin: 0;
    padding: 0;
    height: 100%;
  }
}
</style>

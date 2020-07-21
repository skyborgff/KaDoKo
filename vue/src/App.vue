<template>
  <div id="app">
    <script type=text/javascript src=/eel.js></script>
    <NavBar />
    <Main />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import Main from './components/Main.vue'

export default {
  name: 'app',
  components: {
    NavBar,
    Main
  }
}
</script>

<style>
@import "https://cdn.materialdesignicons.com/2.5.94/css/materialdesignicons.min.css";
@import "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons";

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh
}
  html{
    height: 100vh;
  }
    body{
    height: 100vh;
  }
</style>

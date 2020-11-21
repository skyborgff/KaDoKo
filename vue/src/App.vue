<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'app',
  components: {
  },
  data: function() {
    return {
      first: false,
    }
  },
  mounted: function() {
    var nav = this.$router
    window.eel.expose(route_to, 'route_to'); // Expose this function to Python
    function route_to(destination) {
        nav.push(destination[0])
    }
  },
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

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
  },
}
</script>

<style>
  /*https://github.com/Templarian/MaterialDesign/issues/5608*/
/*@import "https://cdn.materialdesignicons.com/2.5.94/css/materialdesignicons.min.css";*/
@import "https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css";
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

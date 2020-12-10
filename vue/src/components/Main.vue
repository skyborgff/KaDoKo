<template>

<main class="container-fluid h-100" >
      <NavBar />
    <div class="row bg-dark h-100">
        <SideBar />
        <div role="main" class="col px-md-4 bg-dark text-light flex-grow-1 h-100">
            <router-view></router-view>
        </div>
    </div>
</main>


</template>

<script>
import NavBar from './NavBar.vue'
import SideBar from './SideBar.vue'

export default {
  name: 'app',
  components: {
  NavBar,
    SideBar,
  }
}
</script>

<style>
    main{
        padding-top: 40px;
    }
</style>
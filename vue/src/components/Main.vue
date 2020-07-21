<template>
<div class="container-fluid h-100" style="padding-top: 2rem!important">
    <div class="row bg-dark h-100">
        <SideBar />
        <main role="main" class="col px-md-4 bg-dark text-light flex-grow-1 ">
            <router-view></router-view>
        </main>
    </div>
</div>


</template>

<script>
import SideBar from './SideBar.vue'

export default {
  name: 'app',
  components: {
    SideBar,
  }
}
</script>

<style>
    p-t-40{
        padding-top: 40px;
    }
</style>
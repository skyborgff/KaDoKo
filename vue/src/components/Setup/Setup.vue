<template>
<div class="container-fluid h-100" fill-height style="padding-top: 0">
    <div class="row bg-dark h-100" fill-height>
        <router-view></router-view>
    </div>
</div>
</template>

<script>

export default {
  name: 'app',
  components: {
  },
    mounted: function(){
    }
}
</script>

<style>
    p-t-40{
        padding-top: 40px;
    }
</style>

// Note to self:
// I was setting up the options and authenticate part
// Need to add more options on the first screen
// Like what optional libraries and databases to use
// In dev mode I could maybe show the full javascript
// On the bottom
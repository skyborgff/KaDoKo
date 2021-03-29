<template>
  <div>
    <div v-for="anime in anime_listing" :key="anime.name">
      <AnimeCard :anime="anime"></AnimeCard>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import AnimeCard from "./AnimeCard";
  export default {
    name: "AnimeListing",
    components: {AnimeCard},
    data: function(){
      return {anime_listing: []}
    },
    mounted: function(){
      this.get_anime_listing();
    },
    methods: {
      get_anime_listing(){
      const path = 'http://localhost:8283/get_anime_listing';
      axios.get(path).then((res) => {
          this.anime_listing = res.data;
        });
    },
    }
  }
</script>

<style scoped>

</style>
<template>
  <div class="card anime-card mb-3 flex-row bg-dark text-white">
      <img loading=lazy class="card-img-left" :src="anime.logo_url" height="160">
      <div class="card-body">
        <div class="custom-card-title">
          <h5 class="anime-title" ><a href="#">{{anime.title}}</a></h5>
          <h5 class="rating">Rated: {{anime.rating}}/10</h5>
        </div>
        <h6 class="card-subtitle anime-sub-title">{{anime.subtitle}}</h6>
        <div class="card-body anime-description">
          {{anime.description}}
        </div>
        <div class="card-body anime-categories">
          <span v-for="tag in anime.categories" :key="tag" class="badge badge-pill badge-secondary">{{tag}}</span>
        </div>
      </div>
    </div>
</template>

<script>
  export default {
    name: "AnimeCard",
    props: ["anime"]
  }
</script>

<style scoped>
.anime-card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  transition: all 0.3s cubic-bezier(.25,.8,.25,1);
}
.anime-card:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}
.card-body{
  padding: 0.5rem;
  padding-left: 1.5rem;
}
.anime-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  padding-bottom: 0;
  padding-top: 1rem;
}
.custom-card-title{
  display: flex;
  justify-content: space-between;
}
.anime-title{
  width: 80%;
    display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  padding-bottom: 0;
}
  .rating, .anime-sub-title{
    color: #6c757d;
  }
  .card-img-left {
  transition: transform .2s; /* Animation */
  margin: 0 auto;
    z-index: auto;
}

.card-img-left:hover {
  transform: scale(1.5); /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
  z-index: 99999;
}
  .anime-categories{
    display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  padding-bottom: 0;
  }
  .badge {
    margin-right: 0.25rem;
  }
</style>
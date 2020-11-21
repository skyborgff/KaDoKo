<template>
<div class="card" style="width: 18rem;">
  <img src="../../assets/logo.png" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Select your options</h5>
    <p class="card-text">
        Select your main Library
        <select class="custom-select" v-model="Selected_library">
          <option v-for="item in library_list" :value="item.name" :key="item.name">
              {{item.name}}
          </option>
        </select>
        Select your main anime Database
        <select class="custom-select" v-model="Selected_db">
          <option v-for="item in db_list" :value="item.name" :key="item.name">
              {{item.name}}
          </option>
        </select>
    </p>
    <button @click="ButtonAcceptSettings()" type="button" class="btn btn-primary">Continue</button>
  </div>
</div>


</template>

<script>

export default {
  name: 'app',
  components: {
  },
  data: function() {
    return {
      library_list: [],
      db_list: [],
        Selected_db: '',
        Selected_library: '',
    }
  },
  mounted: function() {
    window.eel.library_list()((val) => {
        this.library_list = val;
    });
    window.eel.db_list()((val) => {
        this.db_list = val;
    });
  },
    methods: {
      ButtonAcceptSettings() {
        window.eel.set_start_settings(this.Selected_library, this.Selected_db)()
      },
    }
}
</script>

<style>
    p-t-40{
        padding-top: 40px;
    }
</style>
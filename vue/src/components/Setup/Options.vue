<template>
<div class="card" >
  <img src="../../assets/logo.png" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Select your options</h5>
    <p class="card-text">

      Select your main Library
      <select class="custom-select" v-model="selected_library">
        <option v-for="(library, index) in library_list"
                :value="library" :key="library"
                :selected="index = '0'">
          {{library}}
        </option>
      </select>

      <b-form-group label="Other libraries (sync between them)">
        <b-form-checkbox-group id="checkbox-group-2" v-model="optional_libraries" name="flavour-2">
          <b-form-checkbox v-for="library in library_list"
                           :value="library" :key="library" :disabled="library === selected_library">
            {{library}}
          </b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

      Select your main anime Database
      <select class="custom-select" v-model="selected_db">
        <option v-for="(db, index) in db_list"
                :value="db" :key="db"
                :selected="index === 0">
            {{db}}
        </option>
      </select>

      <b-form-group label="Other databases (more choice of metadata)">
        <b-form-checkbox-group id="checkbox-group-2" v-model="optional_dbs" name="flavour-2">
          <b-form-checkbox v-for="db in db_list"
                           :value="db" :key="db" :disabled="db === selected_db">
            {{db}}
          </b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

        <b-form-group label="Extra options">
          <b-form-checkbox v-model="plex" name="plex" switch>Use Plex</b-form-checkbox>
          <b-form-checkbox v-model="startup" name="startup" switch>Launch on startup</b-form-checkbox>
      </b-form-group>


    </p>
    <button @click="ButtonAcceptSettings()" type="button" class="btn btn-primary">Continue</button>
  </div>

</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'app',
  components: {
  },
  data: function() {
    return {
      library_list: [],
      db_list: [],
      selected_db: '',
      selected_library: '',
      optional_libraries: [],
      optional_dbs: [],
      plex: false,
      startup: false,
    }
  },
  mounted: function() {
    this.getLibraryList();
    this.getDBList();
  },
    methods: {
        getLibraryList() {
          const path = 'http://localhost:8283/library_list';
          axios.get(path).then((res) => {
              this.library_list = res.data;
              this.selected_library = this.library_list[0]
            });
        },
        getDBList() {
          const path = 'http://localhost:8283/db_list';
          axios.get(path).then((res) => {
              this.db_list = res.data;
              this.selected_db = this.db_list[0]
            });
        },
      ButtonAcceptSettings() {
        const path = 'http://localhost:8283/setup_settings';
        var Settings = {
          "selected_library": this.selected_library,
          "selected_db": this.selected_db,
          "optional_libraries": this.optional_libraries,
          "optional_dbs": this.optional_dbs,
          "plex": this.plex,
          "startup": this.startup,
        }
        axios.post(path, Settings)
          .then(() => {
            this.$router.push('/Setup/Authenticate')
          })
      },
    }
}
</script>

<style>
    p-t-40{
        padding-top: 40px;
    }
</style>
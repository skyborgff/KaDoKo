<template>
    <div>
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Settings: Providers</h1>
        </div>
        <div class="container">
            <div class="row">
                <!--Todo: create proper grid with col-->
                <div class="col-sm" v-for="plugin in plugin_info" :key="plugin['name']">
                    <b-card class="card" text-variant="dark" style="width: 18rem; height: 28rem;">
                        <a :href="plugin['website_url']" target="_blank" >
                        <img :src="plugin['logo']" class="card-img-top" alt="..." >
                        </a>
                      <div class="card-body">
                        <h5 class="card-title" :href="plugin['website_url']" >{{plugin['name']}}</h5>
                        <p class="card-text">
                            {{prettifyType(plugin['PluginType'])}}
                            <br>Status: {{plugin['AuthState']}}
                        </p>
                        <button v-if="plugin['AuthState'] !== 'Logged'" @click="GoTo(plugin['url'])" type="button" class="btn btn-primary">Authenticate</button>
                      </div>
                    </b-card>
                </div>
            </div>
            <div class="row">
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
            </div>
            <button @click="ButtonAcceptSettings()" type="button" class="btn btn-primary">Save Settings</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

  export default {
    name: "Providers",
  data: function() {
    return {
      library_list: [],
      db_list: [],
      plugin_info: [],
      selected_db: '',
      selected_library: '',
      optional_libraries: [],
      optional_dbs: [],
    }
  },
  mounted: function() {
    this.getPluginInfo();
    this.getLibraryList();
    this.getDBList();
  },
    methods: {
        prettifyType(list){
            var str = '';
            var counter = 0;
            var size = list.length;
            for (var type in list){
                str += list[type];
                counter += 1;
                if (counter !== size){
                    str += ' | '
                }
            }
            return str
        },
        getPluginInfo() {
          const path = 'http://localhost:8283/plugin_info';
          axios.get(path).then(res => {
              this.plugin_info = res.data;
            });
        },
        getLibraryList() {
          const path = 'http://localhost:8283/library_list';
          axios.get(path).then(res => {
              this.library_list = res.data;
              this.selected_library = this.library_list[0]
            });
        },
        getDBList() {
          const path = 'http://localhost:8283/db_list';
          axios.get(path).then(res => {
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
        }
        axios.post(path, Settings)
          .then(() => {
            this.getLibraryList();
            this.getDBList();
          })
      },
    }
}
</script>

<style scoped>

</style>
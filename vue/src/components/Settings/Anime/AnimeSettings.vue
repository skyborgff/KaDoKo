<template>
  <div>
    <!-- Todo: The drag and drop ordering should become a separate component to be reused -->
    <div class="row">
      <div class="col-sm-7 col-md-5 col-lg-4">
        <h3>Anime Title</h3>
        <div class="form-group">
          <div
            class="bbuttons"
            role="group"
            aria-label="Basic example"
          >
            <button class="btn btn-secondary" @click="add" style="margin: 5px; margin-left: 1px">Add</button>
            <button class="btn btn-secondary" @click="save" style="margin: 5px">Save</button>
          </div>
        </div>
        <draggable
            class="list-group"
            group="people"
            handle=".handle"
            itemKey="name"
            :component-data="{
              tag: 'ul',
              type: 'transition-group',
              name: !drag ? 'flip-list' : null
            }"
            v-model="list"
            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
          >
            <transition-group>
              <div class="card text-white bg-secondary  mb-2" v-for="(element, index) in list" :key="element.language + element.script" >
                <div class="card-body" style="padding: 5px">
                  <table class="table align-middle table-borderless table-sm dropselect" style="margin: 0px; display: inline-block;">
                    <tbody>
                      <tr>
                        <td rowspan='2' class="align-middle"><b-icon icon="arrows-move" class="handle align-middle"></b-icon></td>
                        <th scope="row">Language</th>
                        <td>
                          <select class="form-select " v-model="list[index].language" aria-label="Default select example">
                            <option :selected="language == element.language" v-for="language in languages" :key="language" :value=language>{{language}} </option>
                          </select>
                        </td>
                          <td rowspan='2' class="align-middle"><b-icon icon="x" class="close" @click="removeAt(index)"></b-icon></td>
                      </tr>
                      <tr>
                        <th scope="row">Script</th>
                        <td>
                          <select class="form-select" v-model="list[index].script" aria-label="Default select example">
                            <option :selected="script == element.script" v-for="script in scripts" :key="script" :value=script>{{script}}</option>
                          </select>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </transition-group>
          </draggable>
      </div>
      <div class="col-sm-7 col-md-5 col-lg-4">
        <h3>Anime Sub-Title</h3>
        <div class="form-group">
          <div
            class="bbuttons"
            role="group"
            aria-label="Basic example"
          >
            <button class="btn btn-secondary" @click="add" style="margin: 5px; margin-left: 1px">Add</button>
            <button class="btn btn-secondary" @click="save" style="margin: 5px">Save</button>
          </div>
        </div>
        <draggable
            class="list-group"
            group="people"
            handle=".handle"
            itemKey="name"
            :component-data="{
              tag: 'ul',
              type: 'transition-group',
              name: !drag ? 'flip-list' : null
            }"
            v-model="list"
            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
          >
            <transition-group>
              <div class="card text-white bg-secondary  mb-2" v-for="(element, index) in list" :key="element.language + element.script" >
                <div class="card-body" style="padding: 5px">
                  <table class="table align-middle table-borderless table-sm dropselect" style="margin: 0px; display: inline-block;">
                    <tbody>
                      <tr>
                        <td rowspan='2' class="align-middle"><b-icon icon="arrows-move" class="handle align-middle"></b-icon></td>
                        <th scope="row">Language</th>
                        <td>
                          <select class="form-select " v-model="list[index].language" aria-label="Default select example">
                            <option :selected="language == element.language" v-for="language in languages" :key="language" :value=language>{{language}} </option>
                          </select>
                        </td>
                          <td rowspan='2' class="align-middle"><b-icon icon="x" class="close" @click="removeAt(index)"></b-icon></td>
                      </tr>
                      <tr>
                        <th scope="row">Script</th>
                        <td>
                          <select class="form-select" v-model="list[index].script" aria-label="Default select example">
                            <option :selected="script == element.script" v-for="script in scripts" :key="script" :value=script>{{script}}</option>
                          </select>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </transition-group>
          </draggable>
      </div>
      <div class="col-sm-7 col-md-5 col-lg-4">
        <h3>Anime Description</h3>
        <div class="form-group">
          <div
            class="bbuttons"
            role="group"
            aria-label="Basic example"
          >
            <button class="btn btn-secondary" @click="add" style="margin: 5px; margin-left: 1px">Add</button>
            <button class="btn btn-secondary" @click="save" style="margin: 5px">Save</button>
          </div>
        </div>
        <draggable
            class="list-group"
            group="people"
            handle=".handle"
            itemKey="name"
            :component-data="{
              tag: 'ul',
              type: 'transition-group',
              name: !drag ? 'flip-list' : null
            }"
            v-model="list"
            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
          >
            <transition-group>
              <div class="card text-white bg-secondary  mb-2" v-for="(element, index) in list" :key="element.language + element.script" >
                <div class="card-body" style="padding: 5px">
                  <table class="table align-middle table-borderless table-sm dropselect" style="margin: 0px; display: inline-block;">
                    <tbody>
                      <tr>
                        <td rowspan='2' class="align-middle"><b-icon icon="arrows-move" class="handle align-middle"></b-icon></td>
                        <th scope="row">Language</th>
                        <td>
                          <select class="form-select " v-model="list[index].language" aria-label="Default select example">
                            <option :selected="language == element.language" v-for="language in languages" :key="language" :value=language>{{language}} </option>
                          </select>
                        </td>
                          <td rowspan='2' class="align-middle"><b-icon icon="x" class="close" @click="removeAt(index)"></b-icon></td>
                      </tr>
                      <tr>
                        <th scope="row">Script</th>
                        <td>
                          <select class="form-select" v-model="list[index].script" aria-label="Default select example">
                            <option :selected="script == element.script" v-for="script in scripts" :key="script" :value=script>{{script}}</option>
                          </select>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </transition-group>
          </draggable>
      </div>
      <div class="col-sm-7 col-md-5 col-lg-4">
        <h3>Voice Actors</h3>
        <div class="form-group">
          <div
            class="bbuttons"
            role="group"
            aria-label="Basic example"
          >
            <button class="btn btn-secondary" @click="add" style="margin: 5px; margin-left: 1px">Add</button>
            <button class="btn btn-secondary" @click="save" style="margin: 5px">Save</button>
          </div>
        </div>
        <draggable
            class="list-group"
            group="people"
            handle=".handle"
            itemKey="name"
            :component-data="{
              tag: 'ul',
              type: 'transition-group',
              name: !drag ? 'flip-list' : null
            }"
            v-model="list"
            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
          >
            <transition-group>
              <div class="card text-white bg-secondary  mb-2" v-for="(element, index) in list" :key="element.language + element.script" >
                <div class="card-body" style="padding: 5px">
                  <table class="table align-middle table-borderless table-sm dropselect" style="margin: 0px; display: inline-block;">
                    <tbody>
                      <tr>
                        <td rowspan='2' class="align-middle"><b-icon icon="arrows-move" class="handle align-middle"></b-icon></td>
                        <th scope="row">Language</th>
                        <td>
                          <select class="form-select " v-model="list[index].language" aria-label="Default select example">
                            <option :selected="language == element.language" v-for="language in languages" :key="language" :value=language>{{language}} </option>
                          </select>
                        </td>
                          <td rowspan='2' class="align-middle"><b-icon icon="x" class="close" @click="removeAt(index)"></b-icon></td>
                      </tr>
                      <tr>
                        <th scope="row">Script</th>
                        <td>
                          <select class="form-select" v-model="list[index].script" aria-label="Default select example">
                            <option :selected="script == element.script" v-for="script in scripts" :key="script" :value=script>{{script}}</option>
                          </select>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </transition-group>
          </draggable>
      </div>
      <div class="col-sm-7 col-md-5 col-lg-4">
        <h3>Aditional</h3>
        <div class="form-group">
          <input class="form-check-input" type="checkbox" value="" id="forceDifferentSubtitle">
          <label class="form-check-label" for="forceDifferentSubtitle">
            Force Title and Subtitle to differ
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import draggable from 'vuedraggable'
  let id = 1;
  export default {
    name: "AnimeSettings",
    components: {
      draggable,
    },
    data() {
      return {
        list: [
          { language: "eng", script: "Latn" },
          { language: "jpn", script: "Latn" },
          { language: "jpn", script: "Jpan" },
        ],
        languages: ["afr", "ara", "bul", "cat", "ces", "dan", "deu", "ell", "eng",
          "epo", "est", "fas", "fin", "fra", "glg", "heb", "hin", "hrv", "hun", "ind",
          "isl", "ita", "jpn", "kor", "lav", "lit", "mis", "mon", "msa", "mya", "nan",
          "nld", "nor", "oav", "pol", "por", "prc", "ron", "rus", "slk", "slv", "spa",
          "srp", "swe", "tam", "tgl", "tha", "tur", "ukr", "und", "urd", "vie", "yue",
          "zho",  "none"],
        scripts: ["Latn", "Hant", "Hans", "TWN", "HKG", "BRA", "SGP", ""],
        drag: false
      };
    },
    methods: {
      add: function() {
        for (const index in this.list){
          if (this.list[index].language == "none" &&  this.list[index].script == ""){
            this.list.splice(index, 1)
            break
          }
        }
          this.list.unshift({ language: "none", script: "" });
      },
      replace: function() {
        this.list = [{ name: "Edgard", id: id++ }];
      },
      removeAt(idx) {
      this.list.splice(idx, 1);
      },
      save(idx) {
      this.list.splice(idx, 1);
      },
      clone: function(el) {
        return {
          name: el.name + " cloned"
        };
      },
    },
    computed: {
    dragOptions() {
      return {
        animation: 200,
        group: "description",
        disabled: false,
        ghostClass: "ghost"
      };
    }
    }
  }
</script>

<style scoped>
  .handle {
    width: 30px; height: 30px;
    cursor: move;
    margin-right: 10px;
}
.close {
  float: right;
}
.button {
  margin-top: 35px;
}
.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.list-group-item {
  cursor: move;
}
</style>


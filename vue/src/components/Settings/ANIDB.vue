<template>
    <div>
        <script type=text/javascript src=/eel.js></script>
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">ANIDB</h1>
        </div>

        <div class="row">
          <div pill v-show="!this.connected"  lg="4" class="col pb-2" variant="dark">
              <b-form inline @submit="onSubmit" @reset="onReset">
                  <b-form-group
                    id="input-group-1"
                    label="username"
                    label-for="input-1"
                  >
                    <b-form-input
                      id="input-1"
                      v-model="form.username"
                      required
                      placeholder="Enter username"
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    id="input-group-2"
                    label="Your Password:"
                    label-for="input-2">
                    <b-form-input
                      id="input-2"
                      v-model="form.password"
                      placeholder="Enter password"
                      type="password"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-button type="submit" variant="primary">Submit</b-button>
            </b-form>
          </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'MALUserInfo',
    data: function() {
        return {
            connected: false,
            form: {
              username: '',
              password: '',
            },
        }
    },
    mounted: function() {
        eel.ANIDBConnected()((val) => {
            this.connected = val;
        });
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
          eel.ANIDBConnect(this.form)((val) => {
                this.connected = val;
            })

      },
    },
}
</script>


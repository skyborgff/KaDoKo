<template>
  <div>
<div v-for="authenticator in OAuth_list" :key="authenticator['name']" class="card" style="width: 18rem;">
  <img :src="authenticator['logo_url']" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Select your options</h5>
    <p class="card-text">
        {{authenticator['name']}}
    </p>
    <button @click="GoTo(authenticator['url'])" type="button" class="btn btn-primary">Authenticate</button>
  </div>
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
      OAuth_list: [],
      UserPass_list: [],
      got_reply: false
    }
  },
  mounted: function() {
    this.check_auth();
    this.get_authentication_needed();
  },
  methods: {
    check_auth(){
      var query = this.$route.query;
      if (Object.keys(query).length !== 0){
        var code = query.code;
        var module = this.$route.params.module;
        const path = 'http://localhost:8283/set_authentication';
        axios.post(path, {'module': module, 'code': code})
          .then(() =>{
            this.$router.push(this.$route.path)
            this.get_authentication_needed()
          })
      }
    },
    check_empty(){
      if (this.OAuth_list.length === 0 && this.UserPass_list.length === 0 && this.got_reply){
        this.$router.push('/Main')
      }
      this.$router.push(this.$route.path)
    },
    get_authentication_needed() {
      const path = 'http://localhost:8283/get_authentication_needed';
      axios.get(path).then((res) => {
          this.OAuth_list = res.data['OAuth'];
          this.UserPass_list = res.data['UserPass'];
          this.got_reply = true
          this.check_empty();
        });
    },
    GoTo(destination){
        window.location.href = destination;
    }
  }
}
</script>

<style>
    p-t-40{
        padding-top: 40px;
    }
</style>
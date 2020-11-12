<template>
    <div>
        <script type=text/javascript src=/eel.js></script>
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">My Anime List</h1>
            <b-button pill class="mb-2 mb-md-0" @click="ButtonRefresh()" >
                <b-icon id="ButtonRefresh" icon="arrow-clockwise"></b-icon>
            </b-button>
            <b-button pill class="mb-2 mb-md-0" @click="ButtonMALANIDB()" >Connect MAL to ANIDB</b-button>
        </div>

        <div class="row">
          <div pill v-show="!this.connected"  lg="4" class="col pb-2" variant="dark"><b-button size="lg" @click="ButtonConnect">Connect</b-button></div>
        </div>

        <div class="row"><!-- User row -->
            <div class="col-fluid p-3">
              <b-img class="m1" id="MALAvatar" thumbnail fluid src="https://cdn.myanimelist.net/images/questionmark_50.gif" style="width: 200px; height: 200px" alt="Image 1"></b-img>
            </div>
            <div class="col-fluid p-3">
                <div class="row">
                    <ul id="UserInfo">
                        <li v-for="(value, name, index) in this.UserInfoJson" v-bind:key="index">
                            {{ UserKey[name] }}: {{ value }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="container-fluid">
            <b-row cols="2">
                <div class="col-3">
                    <h2 class="h2">Statistics:</h2>
                </div>
                <div class="col-9">
                    <h2 class="h2">{{$route.path.split('/')[$route.path.split('/').length -1] + ':'}}</h2>
                </div>
                <div class="col-3">
                    <b-list-group id="MainStats" v-for="(value, name, index) in this.MainStatsJson" v-bind:key="index">
                        <b-list-group-item class="d-flex justify-content-between align-items-center" :to="'/Settings/MAL/' + name" variant="dark">
                                {{ name }}:
                            <b-badge variant="primary" class="float-right" pill>{{ value }}</b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </div>

                <div class="col-9 pl-0">
                    <ul id="anime" class="pl-0">
                        <div class="container-fluid pl-0" v-for="(type) in StatusTypes" v-bind:key="value">
                            <div class="container-fluid" v-for="(value) in AnimeInfoJson[type]" v-bind:key="value['node']['id']">
                                <div v-show="type==name_key[$route.path.split('/')[$route.path.split('/').length -1]]" class="container-fluid pl-0">
                                    <b-card :img-src="value['node']['main_picture']['medium']" :img-alt="value['node']['title']" img-left class="mb-3" bg-variant="dark" text-variant="white" img-height="135">
                                        <b-card-text>
                                            {{ value['node']['title'] }}
                                        </b-card-text>
                                        <b-button pill :href="'https://myanimelist.net/anime/' + value['node']['id']" size="sm" target="_blank" variant="outline-light">MAL Link</b-button>
                                        <b-button v-if="GetAIDFromMID(value['node']['id']) != '0'" pill :id="'button-aid-' + type + '-' + value['node']['id']" :href="'https://anidb.net/anime/' + GetAIDFromMID(value['node']['id'])" size="sm" target="_blank" variant="outline-light">ANIDB Link</b-button>
                                        <b-button v-else pill disabled :id="'button-aid-' + type + '-' + value['node']['id']" :href="'https://anidb.net'" size="sm" target="_blank" variant="outline-light">ANIDB Link</b-button>
                                    </b-card>
                                </div>
                            </div>
                        </div>
                    </ul>
                </div>
            </b-row>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MALUserInfo',
    data: function() {
        return {
            UserInfoJson: "",
            UserStatsJson:"",
            MainStatsJson:"",
            AnimeInfoJson:"",
            UserPicture:"https://cdn.myanimelist.net/images/questionmark_50.gif",
            connected: true,
            view: 'watching',
            StatusTypes: [
            'watching',
            'completed',
            'plan_to_watch',
            'on_hold',
            'dropped',
            'Total'
            ],
            name_key: {
            'Watching': 'watching',
            'MAL': 'watching',
            'Completed': 'completed',
            'On Hold': 'on_hold',
            'Plan To Watch': 'plan_to_watch',
            'Dropped': 'dropped',
            'Total': 'Total',
            },
            UserKey: {
            "num_items_watching": "Watching",
            "num_items_completed": "Completed",
            "num_items_on_hold": "On hold",
            "num_items_dropped": "Dropped",
            "num_items_plan_to_watch": "PTW",
            "num_items": "Total",
            "num_days_watched": "Days watched",
            "num_days_watching": "Days watching",
            "num_days_completed": "Days completed",
            "num_days_on_hold": "Days on hold",
            "num_days_dropped": "Days dropped",
            "num_days": "Total Days",
            "num_episodes": "Total Episodes",
            "num_times_rewatched": "Rewatched",
            "mean_score": "Mean score",
            "id": "ID",
            "name": "Name",
            "location": "Location",
            "joined_at": "Joined at"
            },
        }
    },
    mounted: function() {
        this.MALAuthCode(this.$route.query.code);
        eel.MALConnected()((val) => {
            this.connected = val;
        });
        this.GetConnections()
        this.MALUserInfo();
        this.MALAnimeInfo();
    },
    methods: {
        ButtonConnect() {
            eel.MALConnect()((val) => {
                if (!this.connected) {
                    window.location.href = val;
                } else {
                    alert('already connected but tried to connect again')
                }
            })
        },
        ButtonRefresh() {
            eel.MALRefresh();
            this.MALUserInfo();
            this.MALAnimeInfo;
        },
        ButtonMALANIDB() {
            eel.MALANIDBConnect();
        },
        MALConnected() {
            eel.MALConnected()((val) => {
                this.connected = val
            })
        },
        MALUserInfo() {
            if (this.connected) {
                eel.MALUserInfo()((val) => {
                    if (val) {
                        this.UserStatsJson = val.anime_statistics;
                        this.MainStatsJson = val.main_statistics;
                        if (val.picture != undefined) {
                            document.getElementById("MALAvatar").src = val.picture;
                        }
                        delete val.picture;
                        delete val.anime_statistics;
                        delete val.main_statistics;
                        this.UserInfoJson = val
                    }
                })
            }
        },
        MALAnimeInfo() {
            if (this.connected) {
                eel.MALAnimeInfo()((animelist) => {
                    if (animelist) {
                        this.AnimeInfoJson = animelist
                    }
                })
            }
        },
        MALAuthCode(query) {
            if (query != undefined){
                eel.MALAuthCode(query)((val) => {
                    if (val=="True"){
                        window.location.href = (location.toString().split('?')[0] + 'Completed');
                        this.MALConnected();
                        this.MALUserInfo();
                    }
                })
            }
        },
        GetConnections() {
            if (this.connected) {
                eel.GetConnections()((Connections) => {
                    if (Connections) {
                        this.Connections = Connections
                    }
                })
            }
        },
        GetAIDFromMID(mid) {
            for (var connection in this.Connections){
                if (this.Connections[connection]['ids']['MAL'] == mid){
                    var aid = this.Connections[connection]['ids']['AIDB']
                    return aid
                }
            }
            return '0'
        },
    },
}
</script>


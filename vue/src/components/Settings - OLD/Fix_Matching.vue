<template>
    <div>
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Fix Matches</h1>
        </div>

        <div v-for="(anime, index) in Connections" v-bind:key="index">
            <div v-show="parseInt(anime['connected'])==0">
                <div v-for="(value) in AnimeInfoJson.Total" v-bind:key="value">
                    <div v-if="parseInt(value['node']['id'])==parseInt(anime['ids']['MAL'])">
                        <b-card bg-variant="dark" text-variant="white" :title="value['node']['title']" :sub-title="'MAL ID: ' + value['node']['id']" img-left :img-src="value['node']['main_picture']['medium']">
                            <b-card-text>
                                Select the correct anime:
                            </b-card-text>
                            <b-button :href="'https://myanimelist.net/anime/' + value['node']['id']" target="_blank" variant="primary">MAL Anime Link</b-button>
                            <b-form-group stacked>
                                <div v-for="(anime_name) in anime['name_list']" v-bind:key="anime_name">
                                    <b-form-radio v-model="selectedAnime[value['node']['id']]" :name="value['node']['title']" :value="anime_name['id']">
                                    <b-link :href="'https://anidb.net/anime/' + anime_name['id']" target="_blank" class="card-link">{{anime_name['name']}}</b-link></b-form-radio>
                                </div>
                            </b-form-group>
                            <b-input-group prepend="aniDB Id:" class="mt-3">
                                <b-form-input v-model="selectedAnime[value['node']['id']]" type="number" style="max-width: 15%" no-wheel="true" :value="selectedAnime[value['node']['id']]"></b-form-input>
                                <b-input-group-append>
                                    <b-button variant="outline-success" @click="ButtonConnectShows(value['node']['id'], selectedAnime[value['node']['id']])">Accept</b-button>
                                </b-input-group-append>
                            </b-input-group>
                        </b-card>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'MALUserInfo',
    data: function() {
        return {
            AnimeInfoJson:"",
            Connections:"",
            connected: true,
            view: 'watching',
            selectedAnime: {},
            name_key: {
            'Watching': 'watching',
            'MAL': 'watching',
            'Completed': 'completed',
            'On Hold': 'on_hold',
            'Plan To Watch': 'plan_to_watch',
            'Dropped': 'dropped',
            'Total': 'Total',
            },
        }
    },
    mounted: function() {
        window.eel.MALConnected()((val) => {
            this.connected = val;
        });
        this.GetConnections();
        this.MALAnimeInfo();
    },
    methods: {
        ButtonConnect() {
            window.eel.MALConnect()((val) => {
                if (!this.connected) {
                    window.location.href = val;
                } else {
                    alert('already connected but tried to connect again')
                }
            })
        },
        ButtonConnectShows(mid, aid) {
            window.eel.ConnectShows(mid, aid)()
        },
        MALConnected() {
            window.eel.MALConnected()((val) => {
                this.connected = val
            })
        },
        MALAnimeInfo() {
            if (this.connected) {
                window.eel.MALAnimeInfo()((animelist) => {
                    if (animelist) {
                        this.AnimeInfoJson = animelist
                    }
                })
            }
        },
        GetConnections() {
            if (this.connected) {
                window.eel.GetConnections()((Connections) => {
                    if (Connections) {
                        this.Connections = Connections
                    }
                })
            }
        },
    },
}
</script>


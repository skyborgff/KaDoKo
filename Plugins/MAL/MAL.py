from Core.Plugins.Base.BaseLibrary import BaseLibrary
from Core.Plugins.Base.BaseMetadata import BaseMetadata
from Core.Plugins.Base.Auth.OAuth import OAuth
import requests
import json
from ratelimiter import RateLimiter
from Core.Utils.AsyncRateLimiter import AsyncRateLimiter
import time
import Plugins.MAL.Utils.MALFormatter as MALFormatter
from Plugins.MAL.Utils.CachingHeuristic import MALHeuristic
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from Core.Database.Database import Database
import Core.Structures.Anime as AnimeStruct




URL_MAIN = "https://api.myanimelist.net/v2"
URL_SEARCH = "/anime?q={title}&limit={limit}"
URL_DETAILS = "/anime/{id}"
URL_USER = "/users/{user_name}?fields=anime_statistics'"
URL_ANIME_LIST = "/users/{user_name}/animelist"
ANIME_ALL_FIELDS = '?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'


def limited(until):
    duration = int(round(until - time.time()))
    print(f'MAL: Rate limiting, sleeping for {duration} seconds')


class MAL(BaseLibrary, BaseMetadata):
    def __init__(self):
        super().__init__()
        self.name = "MAL"
        self.logo_url = 'https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png'
        self.website_url = 'https://myanimelist.net/'
        client_id = "add1ed488bd218c2e10146345377a0b8"
        url_auth = "https://myanimelist.net/v1/oauth2/authorize"
        url_token = "https://myanimelist.net/v1/oauth2/token"
        self.authenticator = OAuth(self.name, client_id, url_auth, url_token)
        self.requests_session = CacheControl(requests.Session(), cache=FileCache('.Cache/MAL'), heuristic=MALHeuristic())
        # self.requests_session = requests.Session()
        self.rate_limiter = AsyncRateLimiter(max_calls=100, period=1, callback=limited)

    # Currently MAL is not rate limiting, but if it starts, i'll leave this here.
    def load(self, url):
        header = {"Authorization": str(self.authenticator.token_type + " " + self.authenticator.token)}
        with self.rate_limiter:
            result = self.requests_session.get(url, headers=header)
        try:
            if result.from_cache:
                # deletes last call if it was cached. only real api calls need to be slowed down
                self.rate_limiter.calls.pop()
        except: pass
        if result.ok:
            return json.loads(result.content)
        else:
            print(result.content)
            raise RuntimeError('Failed to grab data')

    def Lists(self):
        print("MAL: Obtaining User list")
        all_fields = "?fields=list_status&limit=1000"
        url = URL_MAIN + URL_ANIME_LIST.format(user_name="@me") + all_fields
        # Todo: implement paging
        list = self.load(url)['data']
        AnimeList = MALFormatter.AnimeList(list)
        return AnimeList

    def PopulateAnime(self, database: Database, anime_hash: str):
        oldAnimeData = AnimeStruct.Anime.from_db(anime_hash, database)
        if oldAnimeData.id.getID("MAL"):
            malID = oldAnimeData.id.getID("MAL")
            print(f"MAL: Obtaining Anime Metadata: {malID}")
            url = URL_MAIN + URL_DETAILS.format(id=str(malID)) + ANIME_ALL_FIELDS
            anime_metadata = self.load(url)
            properAnime = MALFormatter.AnimeMetadata(anime_metadata, oldAnimeData)
            # remove edges to stop the anime from keeping some old info like type
            database.remove_successor_edges(oldAnimeData.hash)
            properAnime.to_db(database)


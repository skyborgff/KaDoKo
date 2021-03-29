from Core.Plugins.Base.BaseMetadata import BaseMetadata
import Core.Structures.Anime as AnimeStruct
import Core.Plugins.Base.Flags as Flags
import Plugins.Animeshon.Utils.queries as queries
import Plugins.Animeshon.Utils.AnimeshonFormatter as AnimeshonFormatter
import json
import time
# Todo: centralize this
from Plugins.MAL.Utils.CachingHeuristic import MALHeuristic
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
import requests
from Core.Database.Database import Database
from typing import List
import requests_cache
from ratelimiter import RateLimiter
from Core.Utils.AsyncRateLimiter import AsyncRateLimiter
from Core.Structures.Utils.db_functions import *

LOGO_LIST = ["https://cdn-us.animeshon.com/brand/logo-centered-small-1080.png",
             "https://cdn-us.animeshon.com/brand/logo-no-text-2200.png",
             "https://cdn-us.animeshon.com/brand/logo-no-text-background-white-2600.png",
             "https://cdn-us.animeshon.com/brand/logo-text-400.png",
             "https://cdn-us.animeshon.com/brand/logo-text-background-white-400.jpg",
             "https://cdn-us.animeshon.com/brand/logo-text-large-3200.png"]

def limited(until):
    duration = round(until - time.time(), 5)
    print(f'Animeshon: Rate limiting, sleeping for {duration} seconds', flush=True)

class Animeshon(BaseMetadata):
    def __init__(self):
        super().__init__()
        self.name = "Animeshon"
        self.logo_url = LOGO_LIST[5]
        self.website_url = 'https://animeshon.com/e/'
        self.metadata_flags = [Flags.MetadataFlag.MetadataLinker]
        self.requests_session = CacheControl(requests.Session(),
                                             cacheable_methods=("POST", "GET"),
                                             cache=FileCache('.Cache/Animeshon'),
                                             heuristic=MALHeuristic())
        # Note To Self: CacheControl uses the url as a key.
        #  Post requests use the same url. research alternatives like requests-cache
        #  https://github.com/ionrock/cachecontrol/issues/216

        self.requests_session = requests_cache.core.CachedSession(cache_name='.Cache/Animeshon/cache',
                                                                  backend='sqlite',
                                                                  expire_after=60*60*24*365,  # 1 Year Cache
                                                                  allowable_methods=('GET', 'POST'),
                                                                  include_get_headers=True)
        self.uncached_requests_session = requests.Session()
        self.getratelimiter = AsyncRateLimiter(max_calls=20, period=1, callback=limited)
        self.queryratelimiter = AsyncRateLimiter(max_calls=10, period=1, callback=limited)




    def query(self, query: str, query_type:str = 'query'):
        url = "https://api.animeshon.com/graphql"
        if query_type == 'query':
            rate_limiter = self.queryratelimiter
        elif query_type == 'get':
            rate_limiter = self.getratelimiter
        with rate_limiter:
            result = self.requests_session.post(url, json={'query': query})
            try:
                if result.from_cache:
                    # deletes last call if it was cached. only real api calls need to be slowed down
                    rate_limiter.calls.pop()
            except: pass
        if result.ok:
            if result.from_cache:
                error_on_cache = json.loads(result.content).get('errors')
                if error_on_cache:
                    key = self.requests_session.cache.create_key(result.request)
                    self.requests_session.cache.delete(key)
                    return self.query(query, query_type)
            return json.loads(result.content), result
        else:
            print(result.content)
            raise RuntimeError('Failed to grab data')

    def LinkId(self, metaIDs: AnimeStruct.MetaIDs):
        namespace_dict = {"MAL": "myanimelist-net",
                          "ANIDB": "anidb-net",
                          "ANN": "animenewsnetwork-com"}
        plugin_namespace_dict = {"myanimelist-net": "MAL",
                                 "anidb-net": "ANIDB",
                                 "animenewsnetwork-com": "ANN"}
        mappedPlugins = metaIDs.mappedPlugins()
        if "MAL" in mappedPlugins and "ANIDB" in mappedPlugins and "ANN" in mappedPlugins and "Animeshon" in mappedPlugins:
            return metaIDs
        for metaId in metaIDs.list:
            if metaId.PluginName in namespace_dict.keys():
                namespace = namespace_dict[metaId.PluginName]
                externalID = metaId.id
                query = queries.queryCrossReference.format(externalID=externalID, namespace=namespace)
                print(f"Animeshon: Linking ids from: {metaId.PluginName} : {metaId.id}")
                queryReply, raw = self.query(query, 'query')
                result = queryReply.get("data")
                if not result.get("queryCrossReference"):
                    # Todo: This may also be true if we are being rate limited!
                    if result.get('errors'):
                        raise RuntimeError(result.get('errors')[0].get('message'))
                    else:
                        print('Not Found')
                    # Delete from cache so next time it may have been added
                    key = self.requests_session.cache.create_key(raw.request)
                    self.requests_session.cache.delete(key)
                    return metaIDs
        anime_data = result.get("queryCrossReference")[0].get("resource")
        Animeshon_Metaid = AnimeStruct.MetaID(self.name, anime_data.get("id"))
        metaIDs.list.append(Animeshon_Metaid)
        for meta in anime_data.get("crossrefs"):
            pluginName = plugin_namespace_dict[meta.get("namespace")]
            id = meta.get("externalID")
            if pluginName not in mappedPlugins:
                meta_Metaid = AnimeStruct.MetaID(pluginName, id)
                metaIDs.list.append(meta_Metaid)
        return metaIDs

    def LinkIds(self, database: Database, anime_hash: str):
        """Grabs the anime from the database and adds new
        metadata ids from diferent providers"""
        anime: AnimeStruct.Anime = AnimeStruct.Anime.from_db(anime_hash, database)
        MetaIds: AnimeStruct.MetaIDs = self.LinkId(anime.id)
        MetaIds.to_db(database)

    def PopulateAnime(self, database: Database, anime_hash: str):
        oldAnimeData = AnimeStruct.Anime.from_db(anime_hash, database)
        if oldAnimeData.id.getID("Animeshon"):
            AnimeshonID = oldAnimeData.id.getID("Animeshon")
            query = queries.getAnime.format(AnimeshonID=AnimeshonID)
            print(f"Animeshon: Obtaining Anime Metadata: {AnimeshonID}")
            queryReply, raw = self.query(query, 'get')
            anime_metadata = queryReply.get("data").get('getAnime')
            properAnime = AnimeshonFormatter.AnimeMetadata(anime_metadata, oldAnimeData)
            # remove edges to stop the anime from keeping some old info like type
            database.remove_successor_edges(oldAnimeData.hash)
            properAnime.to_db(database)

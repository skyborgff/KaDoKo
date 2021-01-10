from Core.Plugins.Base.BaseMetadata import BaseMetadata
import Core.Structures.Anime as AnimeStruct
import Core.Plugins.Base.Flags as Flags
import Plugins.Animeshon.Utils.queries as queries
from ratelimiter import RateLimiter
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

def limited(until):
    duration = int(round(until - time.time()))
    print(f'Animeshon is being rate limited, sleeping for {duration} seconds')

class Animeshon(BaseMetadata):
    def __init__(self):
        super().__init__()
        self.name = "Animeshon"
        self.logo_url = 'https://animeshon.com/e/_next/static/media/animeshon-brand.5de13d23bcab08ceaeaec5186335d368.svg'
        self.website_url = 'https://animeshon.com/e/'
        self.metadata_flags = [Flags.MetadataFlag.MetadataLinker]
        self.requests_session = CacheControl(requests.Session(),
                                             cacheable_methods=("POST", "GET"),
                                             cache=FileCache('.Cache/Animeshon'),
                                             heuristic=MALHeuristic())
        self.requests_session = requests_cache.core.CachedSession(cache_name='.Cache/Animeshon/cache',
                                                                  backend='sqlite',
                                                                  expire_after=60*60*24*7,
                                                                  allowable_methods=('GET', 'POST'),
                                                                  include_get_headers=True)
        # self.requests_session = requests.Session()
        self.getratelimiter = RateLimiter(max_calls=30, period=30, callback=limited)
        self.queryratelimiter = RateLimiter(max_calls=10, period=30, callback=limited)

    # Note To Self: CacheControl uses the url as a key.
    #  Post requests use the same url. research alternatives like requests-cache
    #  https://github.com/ionrock/cachecontrol/issues/216


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
                print(f"Animeshon: Linking ids from: {metaId.PluginName} : {metaId.id}")
                namespace = namespace_dict[metaId.PluginName]
                externalID = metaId.id
                query = queries.queryCrossReference.format(externalID=externalID, namespace=namespace)
                queryReply, raw = self.query(query, 'query')
                result = queryReply.get("data")
                if not result.get("queryCrossReference"):
                    print('Not Found')
                    return metaIDs
        anime_data = result.get("queryCrossReference")[0].get("content")
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
            print(f"Animeshon: Obtaining Anime Metadata: {AnimeshonID}")
            query = queries.getAnime.format(AnimeshonID=AnimeshonID)
            queryReply, raw = self.query(query, 'get')
            anime_metadata = queryReply.get("data").get('getAnime')
            properAnime = AnimeshonFormatter.AnimeMetadata(anime_metadata, oldAnimeData)
            # remove edges to stop the anime from keeping some old info like type
            database.remove_successor_edges(oldAnimeData.hash)
            properAnime.to_db(database)

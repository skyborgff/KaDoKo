import os
import json
from datetime import datetime, timedelta
import secrets
import webbrowser
from urllib.parse import urlencode
import requests
import json
from .api import *
from .OAuth import OAuth
from time import time, sleep
import eel
from Utils.Cache import Cache
from itertools import groupby


AUTH_FILE = 'API/MAL/MAL_Auth.json'
CLIENT_FILE = 'API/MAL/client_id.txt'
Module_Name = os.path.join('Clients', 'MAL')
Relations_FILE = 'API/MAL/relations.json'

#self.info_cache = Cache(Module_Name=Module_Name, SubModule_Name='info', validity='1M')
#self.user_cache = Cache(Module_Name=Module_Name, SubModule_Name='user', validity='30m')

class Defaults:
    def __init__(self):
        self.submodule = 'info'
        self.validity = '1M'

class Client:
    def __init__(self, cache):
        self.Module = 'MAL'
        self.cache = cache
        # Authentication for MAL api. It handles the token creation / refreshing
        self.auth = OAuth()
        # This status is used to know if we are authenticated, or if we need to give a code
        self.status = self.auth.service(AUTH_FILE, CLIENT_FILE)  # False = need code, true = all good bro, keep apiing
        self._last_request = 0
        if os.path.exists(Relations_FILE):
            with open(Relations_FILE) as file:
                self.relations = json.load(file)
        else:
            self.relations = []

    # if its the first authentication we need to provide the user code after he accepts stuff
    def finish_auth(self, code):
        self.auth.auth_session(code)
        self.status = True
        return

    # General function to grab urls from the api
    def load(self, url):
        # rate limiting
        if (time() - self._last_request) < 3:
            eel.sleep(3 - time() - self._last_request)
        result = requests.get(url, headers={"Authorization": self.auth.get_header()})
        if result.ok:
            return json.loads(result.content)
        else:
            print(result.content)
            raise RuntimeError('Failed to grab data')

    def refresh(self):
        self.cache.refresh(self.Module, 'info')
        self.cache.refresh(self.Module, 'user')

    # Search the API for the id of the Anime
    def anime(self, anime_id):
        all_fields = '?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
        url = URL_MAIN + URL_DETAILS.format(id=str(anime_id)) + all_fields
        if self.cache.valid('anime', self.Module, 'info'):
            data = self.cache.get('anime', self.Module, 'info')
        else:
            data = self.load(url)
            self.cache.save(data, 'anime', self.Module, 'info')
        return data

    # Search the API for the name of the Anime
    def search(self, name, limit=20):
        url = URL_MAIN + URL_SEARCH.format(title=name, limit=limit)
        if self.cache.valid('search', self.Module, 'info'):
            data = self.cache.get('search', self.Module, 'info')
        else:
            data = self.load(url)
            self.cache.save( data, 'search', self.Module, 'info')
        return data

    # Ask the API for the user info
    def user(self, name):
        url = URL_MAIN + URL_USER.format(user_name=name)
        if self.cache.valid('user', self.Module, 'user'):
            data = self.cache.get('user', self.Module, 'user')
        else:
            data = self.load(url)
            self.cache.save(data, 'user', self.Module, 'user', '30m')
        # Separate statistics into Main and All so we can do v-for without v-if
        data['main_statistics'] = {}
        data['main_statistics']['Watching'] = data['anime_statistics']['num_items_watching']
        data['main_statistics']['Completed'] = data['anime_statistics']['num_items_completed']
        data['main_statistics']['On Hold'] = data['anime_statistics']['num_items_on_hold']
        data['main_statistics']['Dropped'] = data['anime_statistics']['num_items_dropped']
        data['main_statistics']['Plan To Watch'] = data['anime_statistics']['num_items_plan_to_watch']
        data['main_statistics']['Total'] = data['anime_statistics']['num_items']
        return data

    # Ask the API for the user anime list
    def anime_list(self, name):
        all_fields = "?fields=list_status&limit=10000"
        url = URL_MAIN + URL_ANIME_LIST.format(user_name=name) + all_fields
        # Todo: implement paging
        if self.cache.valid('anime_list', self.Module, 'user'):
            data = self.cache.get('anime_list', self.Module, 'user')
        else:
            data = self.load(url)['data']
            self.cache.save(data, 'anime_list', self.Module, 'user')

        # We do the sorting so it shows in order in vue
        data.sort(key=lambda x: int(x['node']['id']), reverse=True)
        # Grouping so we can separate them without v-if
        grouped = {}
        for elem in data:
            key = elem['list_status']['status']
            grouped.setdefault(key, []).append(elem)
            grouped.setdefault('Total', []).append(elem)
        return grouped


    def get_related(self, mal_id, relation_type=''):
        anime_info = self.anime(mal_id)
        related_list=[]
        related_all_anime = anime_info['related_anime']
        if not relation_type:
            for related_anime in related_all_anime:
                if related_anime['relation_type'] == relation_type or relation_type == '':
                    rel_id = related_anime['node']['id']
                    rel_type = self.anime(rel_id)['media_type']
                    related_list.append({id: rel_id, type: rel_type})
        return related_list

    def generate_series(self, mal_id):

        print('Generation for ' + str(mal_id) + ' started')
        related_list = []
        anime_info = self.anime(mal_id)
        relation_delta = 0
        related_list.append([mal_id, relation_delta])

        prequel_list = self.get_related(mal_id, 'prequel')
        sequel_list = self.get_related(mal_id, 'sequel')

        if len(prequel_list) > 1:
            prequel_id = 0
            for anime in prequel_list:
                if anime['type'] == 'tv':
                    prequel_id = anime['id']
            if not prequel_id:
                prequel_id = prequel_list[0]['id']



        series_list = []
        series_list.append(self.get_info(mal_id))
        print('Prequel start')
        self.add_related(series_list, mal_id, 'Prequel')
        print('Sequel start')
        self.add_related(series_list, mal_id, 'Sequel')
        id_list = []
        for anime in series_list:
            id_list.append(anime['@id'])
        anime_data = {'data': series_list, "ids": id_list, 'added': [mal_id]}
        self.data.append(anime_data)
        self.save_data()
        print('Generation for ' + str(mal_id) + ' ended')
        return anime_data

    def add_related_prequel(self, related, mal_id, relation_delta):
        anime = self.anime(mal_id)
        try:
            self.array(anime['relatedanime'])
        except:
            return
        for related in self.array(anime['relatedanime']['anime']):
            if related['@type'] == relation_type:
                prequel = self.add_related(series_list, related['@id'], relation_type)
                if prequel:
                    series_list.append(prequel)
        if anime['type'] == 'TV Series':
            return anime
        else:
            return
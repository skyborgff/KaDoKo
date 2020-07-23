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


class Client:
    def __init__(self):
        # Authentication for MAL api. It handles the token creation / refreshing
        self.auth = OAuth()
        self.info_cache = Cache(Module_Name=Module_Name, SubModule_Name='info', validity='1M')
        self.user_cache = Cache(Module_Name=Module_Name, SubModule_Name='user', validity='30m')
        # This status is used to know if we are authenticated, or if we need to give a code
        self.status = self.auth.service(AUTH_FILE, CLIENT_FILE)  # False = need code, true = all good bro, keep apiing
        self._last_request = 0

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
        self.info_cache.refresh()
        self.user_cache.refresh()

    # Search the API for the id of the Anime
    def anime(self, anime_id):
        all_fields = '?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
        url = URL_MAIN + URL_DETAILS.format(id=str(anime_id)) + all_fields
        if self.info_cache.valid('anime'):
            data = self.info_cache.get('anime')
        else:
            data = self.load(url)
            self.info_cache.save('anime', data)
        return data

    # Search the API for the name of the Anime
    def search(self, name, limit=20):
        url = URL_MAIN + URL_SEARCH.format(title=name, limit=limit)
        if self.info_cache.valid('search'):
            data = self.info_cache.get('search')
        else:
            data = self.load(url)
            self.info_cache.save('search', data)
        return data

    # Ask the API for the user info
    def user(self, name):
        url = URL_MAIN + URL_USER.format(user_name=name)
        if self.user_cache.valid('user'):
            data = self.user_cache.get('user')
        else:
            data = self.load(url)
            self.user_cache.save('user', data)
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
        all_fields = "?fields=list_status&limit=200"
        url = URL_MAIN + URL_ANIME_LIST.format(user_name=name) + all_fields
        # Todo: implement paging
        if self.user_cache.valid('anime_list'):
            data = self.user_cache.get('anime_list')
        else:
            data = self.load(url)['data']
            self.user_cache.save('anime_list', data)

        # We do the sorting so it shows in order in vue
        data.sort(key=lambda x: int(x['node']['id']), reverse=True)
        # Grouping so we can separate them without v-if
        grouped = {}
        for elem in data:
            key = elem['list_status']['status']
            grouped.setdefault(key, []).append(elem)
            grouped.setdefault('Total', []).append(elem)
        return grouped

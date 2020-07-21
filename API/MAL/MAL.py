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
from .Cache import Cache
from itertools import groupby


AUTH_FILE = 'API/MAL/MAL_Auth.json'
CLIENT_FILE = 'API/MAL/client_id.txt'



class Client:
    def __init__(self):
        self.auth = OAuth()
        self.active = False
        self.cache = Cache(file='API/MAL/CACHE_MAL.json')

    def authenticate(self):
        # if is not true, launch authorization and give code
        auth_reply = self.auth.service(AUTH_FILE, CLIENT_FILE)
        if auth_reply is True:
            self.active = True
        return auth_reply

    def authenticate_code(self, code):
        self.auth.auth_session(code)
        self.active = True
        return

    def load(self, url):
        # try:
        print(url)
        result = requests.get(url, headers={"Authorization": self.auth.get_header()})
        sleep(2)
        print(result)
        if result.ok:
            return json.loads(result.content)
        else:
            print(result.content)
            raise RuntimeError('Failed to grab data')

    def refresh(self):
        self.cache.refresh()

    '''
    Search the API for the id of the Anime
    '''

    def anime(self, anime_id):
        all_fields = '?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
        apiUrl = URL_MAIN + URL_DETAILS.format(id=str(anime_id)) + all_fields
        if self.cache.valid('anime'):
            data = self.cache.get('anime')
        else:
            data = self.load(apiUrl)
            self.cache.save('anime', data)
        return data

    '''
    Search the API for the name of the Anime
    '''

    def search(self, name, limit=20):
        apiUrl = URL_MAIN + URL_SEARCH.format(title=name, limit=limit)
        if self.cache.valid('search'):
            data = self.cache.get('search')
        else:
            data = self.load(apiUrl)
            self.cache.save('search', data)
        return data

    '''
    Search the API for a user
    '''

    def user(self, name):
        apiUrl = URL_MAIN + URL_USER.format(user_name=name)
        if self.cache.valid('user'):
            data = self.cache.get('user')
        else:
            data = self.load(apiUrl)
            self.cache.save('user', data)
        data['main_statistics'] = {}
        data['main_statistics']['Watching'] = data['anime_statistics']['num_items_watching']
        data['main_statistics']['Completed'] = data['anime_statistics']['num_items_completed']
        data['main_statistics']['On Hold'] = data['anime_statistics']['num_items_on_hold']
        data['main_statistics']['Dropped'] = data['anime_statistics']['num_items_dropped']
        data['main_statistics']['Plan To Watch'] = data['anime_statistics']['num_items_plan_to_watch']
        data['main_statistics']['Total'] = data['anime_statistics']['num_items']

        return data

    def anime_list(self, name):
        all_fields = "?fields=list_status&limit=200"
        apiUrl = URL_MAIN + URL_ANIME_LIST.format(user_name=name) + all_fields
        #Todo: implement paging
        if self.cache.valid('anime_list'):
            data = self.cache.get('anime_list')
        else:
            data = self.load(apiUrl)
            data = data['data']
            self.cache.save('anime_list', data)
        data.sort(key=lambda x: int(x['node']['id']), reverse=True)
        grouped = {}
        for elem in data:
            key = elem['list_status']['status']
            grouped.setdefault(key, []).append(elem)
            grouped.setdefault('Total', []).append(elem)
        return grouped

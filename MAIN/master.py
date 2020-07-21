from API.MAL.MAL import Client as MalClient
from API.ANIDB.ANIDB import Client as ANIClient
import os
import json

DB_FILE = 'MAIN/connections.json'

class Master():
    def __init__(self):
        self.mal = MalClient()
        self.anidb = ANIClient()
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = []

    def mal_auth(self):
        return self.mal.authenticate()

    def connect_ids(self, status='watching'):
        status = 'Total'
        self.connections = []
        self.data = []
        missing = []
        print('connecting')
        if not self.mal.active:
            raise Exception('NOT CONNECTED TO MAL')
        anime_list = self.mal.anime_list('@me')
        for anime in anime_list[status]:
            print(anime['node']['title'])
            mid = anime['node']['id']
            matches = self.anidb.search(anime['node']['title'])
            if len(matches) != 1:
                match_info = []
                for name in matches:
                    aid = self.anidb.get_id(name)
                    match_info.append({'name': name, 'id': aid})
                connection = {'ids': {'MAL': mid, 'AIDB': 0},
                              'connected': 0,
                              'name_list': match_info}
            else:
                aid = self.anidb.get_id(matches[0])
                connection = {'ids': {'MAL': mid, 'AIDB': aid},
                              'connected': 1,
                              'name_list': []}
                self.anidb.generate_series(aid)
            self.data.append(connection)
        self.data.sort(key=lambda x: x['ids']['MAL'])
        self.data.sort(key=lambda x: x['connected'])
        self.save_connections()

    def save_connections(self):
        with open(DB_FILE, 'w') as file:
            json.dump(self.data, file, indent=1)

    def get_connections(self):
        with open(DB_FILE, 'r') as file:
            self.data = json.load(file)
        return self.data

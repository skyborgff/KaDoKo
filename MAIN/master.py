from API.MAL.MAL import Client as MalClient
from API.ANIDB.ANIDB import Client as ANIClient
import os
import json
import gevent.monkey
gevent.monkey.patch_all()
import eel

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
            self.save_connections()

    def mal_auth(self):
        return self.mal.status

    def connect_known(self, mid, aidb):
        pass

    def get_connection_info(self, id, type='MAL'):
        connections = self.get_connections()
        for anime in connections:
            if anime['ids'][type] == id:
                return anime

    def connect_ids(self, status='watching'):
        self.connections = self.get_connections()
        self.data = []
        if not self.mal.status==True:
            raise Exception('NOT CONNECTED TO MAL')

        anime_list = self.mal.anime_list('@me')
        for anime in anime_list[status]:
            mid = int(anime['node']['id'])
            mal_title = anime['node']['title']
            print('Connecting: ' + mal_title)

            connection = self.get_connection_info(mid, type='MAL')

            if connection:
                self.data.append(connection)
                print('Already Connected')
            else:
                matches = self.anidb.search(mal_title, count=4)
                if len(matches) > 1:
                    match_info = []
                    for name in matches:
                        aid = self.anidb.get_id(name)
                        match_info.append({'name': name, 'id': aid})
                    connection = {'ids': {'MAL': mid, 'AIDB': 0},
                                  'connected': 0,
                                  'name_list': match_info}
                elif len(matches) == 1:
                    aid = self.anidb.get_id(matches[0])
                    connection = {'ids': {'MAL': mid, 'AIDB': aid},
                                  'connected': 1,
                                  'name_list': []}
                    print('Found match: ' + str(aid) + '\nGenerating series')
                self.data.append(connection)
                self.anidb.generate_series(aid)
            self.save_connections()

    def save_connections(self):
        print('Saving connections')
        with open(DB_FILE, 'w') as file:
            json.dump(self.data, file, indent=1)

    def get_connections(self):
        return self.data

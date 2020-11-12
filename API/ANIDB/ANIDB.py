import json
import xmltodict
import os
import requests
import difflib
from Utils.Cache import Cache
import eel

SEARCH_GZ = 'API/ANIDB/anime-titles.xml.gz'
SEARCH_DB = 'API/ANIDB/anime-titles.xml'
SEARCH_DB_JSON = 'API/ANIDB/anime-titles.json'
DATA_FILE = 'API/ANIDB/data_series.json'
TITLES_LINK = 'https://raw.githubusercontent.com/ScudLee/anime-lists/master/animetitles.xml'


class Client:
    def __init__(self):
        self.cache = Cache(Module_Name='Clients/ANIDB', SubModule_Name='info', validity='1M')
        self.titles_cache = Cache(Module_Name='Clients/ANIDB', SubModule_Name='titles', validity='1w')
        self.DB = self.load_DB()
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as file:
                self.data = json.load(file)
        else:
            self.data = []

    def convert_DB(self):
        with open(SEARCH_DB, 'r', encoding='utf8') as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        json_data = json.loads(json.dumps(data_dict))
        with open(SEARCH_DB_JSON, "w", encoding='utf8') as json_file:
            json.dump(json_data, json_file, indent=1, ensure_ascii=False)
        return json_data

    def load_DB(self):
        if not self.titles_cache.valid('anime-titles') or not os.path.exists(SEARCH_DB_JSON):
            r = requests.get(TITLES_LINK, allow_redirects=True)
            open(SEARCH_DB, 'wb').write(r.content)
            self.titles_cache.save('anime-titles', '')
            self.convert_DB()
        with open(SEARCH_DB_JSON, encoding='utf8') as json_file:
            json_data = json.load(json_file, encoding='utf8')
        return json_data

    def array(self, data):
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]

    def search(self, string, count=4):
        string = string
        titles_list = []
        for anime in reversed(self.DB['animetitles']['anime']):
            titles = self.array(anime['title'])
            anime_titles = []
            for title in titles:
                anime_titles.append(title['#text'])
            closest_title = difflib.get_close_matches(string, anime_titles, n=1)
            if len(closest_title) != 0:
                titles_list.append(closest_title[0])
        closest = difflib.get_close_matches(string, titles_list, n=count)
        if closest and (closest[0].lower() == string.lower()):
            # if direct match just give that one
            closest = [closest[0]]
        return closest

    def get_id(self, anime_name):
        for anime in self.DB['animetitles']['anime']:
            titles = self.array(anime['title'])
            for title in titles:
                    name = title['#text']
                    if name == anime_name:
                        aid = anime['@aid']
                        return int(aid)

    def get_info(self, aid):
        print('asking ANIDB for: ' + str(aid))
        if self.cache.valid(aid):
            print('cached')
            return self.cache.get(aid)
        else:
            print('asking API')
            eel.sleep(3)
            anime_url = 'http://api.anidb.net:9001/httpapi?request=anime&client={client}&clientver={ver}&protover=1&aid={id}'
            url = anime_url.format(client='plexanidbsynchtt', ver='2', id=aid)
            result = requests.get(url)
            parsed = xmltodict.parse(result.content)
            data = json.loads(json.dumps(parsed))
            #print(data)
            try:
                data = data['anime']
                self.cache.save(aid, data)
            except:
                data = {}
        return data

    def save_data(self):
        data_file = 'API/ANIDB/data_series.json'
        with open(data_file, 'w') as file:
            json.dump(self.data, file, indent=1)

    def generate_series(self, aid):
        print('Generation for ' + str(aid) + ' started')

        for series in self.data:
            if aid in series['ids']:
                if aid not in series['added']:
                    series['added'].append(aid)
                    self.save_data()
                return series
        series_list = []
        series_list.append(self.get_info(aid))
        print('Prequel start')
        self.add_related(series_list, aid, 'Prequel')
        print('Sequel start')
        self.add_related(series_list, aid, 'Sequel')
        id_list = []
        for anime in series_list:
            id_list.append(anime['@id'])
        anime_data = {'data': series_list, "ids": id_list, 'added': [aid]}
        self.data.append(anime_data)
        self.save_data()
        print('Generation for ' + str(aid) + ' ended')
        return anime_data

    def add_related(self, series_list, aid, relation_type):
        anime = self.get_info(aid)
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

import json
import xmltodict
import os
import requests
import difflib
import time
from .Cache import Cache

SEARCH_DB = 'API/ANIDB/anime-titles.xml'
SEARCH_DB_JSON = 'API/ANIDB/anime-titles.json'

class Client:
    def __init__(self):
        self.cache = Cache(file='API/ANIDB/CACHE_ANIDB.json')
        self.DB = self.load_DB()

    def load_DB(self):
        if not os.path.exists(SEARCH_DB_JSON):
            with open(SEARCH_DB, 'r', encoding='utf8') as xml_file:
                data_dict = xmltodict.parse(xml_file.read())
            json_data = json.loads(json.dumps(data_dict))
            with open(SEARCH_DB_JSON, "w", encoding='utf8') as json_file:
                json.dump(json_data, json_file, indent=1, ensure_ascii=False)
        else:
            with open(SEARCH_DB_JSON, encoding='utf8') as json_file:
                json_data = json.load(json_file, encoding='utf8')
        return json_data

    def array(self, data):
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]

    def search(self, string):
        string = string
        titles_list = []
        for anime in self.DB['animetitles']['anime']:
            titles = self.array(anime['title'])
            anime_titles = []
            for title in titles:
                anime_titles.append(title['#text'])
            closest_title = difflib.get_close_matches(string, anime_titles, n=1)
            if len(closest_title) != 0:
                titles_list.append(closest_title[0])
        closest = difflib.get_close_matches(string, titles_list, n=4)
        if closest[0].lower() == string.lower():
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
                        return aid

    def get_info(self, aid):
        print(aid)
        if self.cache.valid(aid):
            return self.cache.get(aid)
        else:
            print('asking API')
            time.sleep(3)
            anime_url = 'http://api.anidb.net:9001/httpapi?request=anime&client={client}&clientver={ver}&protover=1&aid={id}'
            url = anime_url.format(client='plexanidbsynchtt', ver='2', id=aid)
            result = requests.get(url)
            parsed = xmltodict.parse(result.content)
            data = json.loads(json.dumps(parsed))
            print(data)
            data = data['anime']
            self.cache.save(aid, data)
        return data

    def generate_series(self, aid):
        data_file = 'API/ANIDB/data_series.json'
        if os.path.exists(data_file):
            with open(data_file) as file:
                data = json.load(file)
        else:
            data = []
        for series in data:
            if aid in series['ids']:
                if aid not in series['added']:
                    series['added'].append(aid)
                    with open(data_file, 'w') as file:
                        json.dump(data, file, indent=1)
                return series
        series_list = []
        series_list.append(self.get_info(aid))
        self.add_related(series_list, aid, 'Prequel')
        self.add_related(series_list, aid, 'Sequel')
        #clear duplicates, possible not needed
        #series_list = list(dict.fromkeys(series_list))
        series_list.sort(key=lambda x: int(x['@id']))
        id_list = []
        for anime in series_list:
            id_list.append(anime['@id'])
        anime_data = {'data': series_list, "ids": id_list, 'added': [aid]}
        data.append({'data': series_list, "ids": id_list, 'added': [aid]})
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=1)
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
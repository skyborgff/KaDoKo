import json
from time import time
import os
import glob

Cache_Folder = 'Cache'
Cache_Map_file = 'Cache/Cache_Map.json'
Validity_dict = {
    '1m': 60,
    '30m': 60*30,
    '1h': 60*60,
    '6h': 60*60*6,
    '12h': 60*60*12,
    '1d': 60*60*24,
    '1w': 60*60*24*7,
    '1M': 60*60*24*30,
}

class Cache:
    def __init__(self):
        if not os.path.exists(Cache_Map_file):
            self.assure_path(Cache_Folder)
            with open(Cache_Map_file, 'w+') as file:
                json.dump({'': ''}, file, indent=1)

    # Adds the data to the cache with timestamp and saves it
    def save(self, data, identifier, module='General', submodule='General', validity='1M', type='json', ensure_ascii=True):
        identifier = str(identifier)
        identifier_file_name = f'{identifier}.{type}'
        folder_path = os.path.join(Cache_Folder, module, submodule)
        file_path = os.path.join(folder_path, identifier_file_name)
        self.assure_path(folder_path)
        with open(Cache_Map_file, 'r') as map_file:
            cache_map = json.load(map_file)
            if module not in cache_map.keys():
                cache_map[module] = {}
                cache_map[module][submodule] = {}
            if submodule not in cache_map[module].keys():
                cache_map[module][submodule] = {}
        with open(Cache_Map_file, 'w') as map_file:
            cache_map[module][submodule][identifier] = {'validity': Validity_dict.get(validity, Validity_dict['1w']),
                                                  'time': int(time()),
                                                  'type': type,
                                                  'location': file_path}
            json.dump(cache_map, map_file, indent=1, ensure_ascii=ensure_ascii)
        if type == 'json':
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=1, ensure_ascii=ensure_ascii)
        else:
            with open(file_path, 'wb') as file:
                file.write(data)

    def get(self, identifier, module='General', submodule='General'):
        info = self.get_info(identifier, module, submodule)
        if not info:
            return None
        type = info['type']
        location = info['location']
        if type == 'json':
            with open(location, 'r', encoding="utf-8") as file:
                return json.load(file)
        else:
            return location

    def get_info(self, identifier, module='General', submodule='General'):
        with open(Cache_Map_file, 'r') as map_file:
            map = json.load(map_file)
            try:
                info = map[module][submodule][identifier]
            except KeyError:
                return None
            else:
                return info

    def valid(self, identifier, module='General', submodule='General'):
        info = self.get_info(identifier, module, submodule)
        if info:
            expired = (time() - int(info['time'])) > int(info['validity'])
            exists = os.path.exists(info['location'])
            return not expired and exists
        else:
            return False

    # Deletes the whole cache so it gets refreshed.
    # TODO: Refresh cache in a better way, so that if api is down you can still use old cache as a fallback
    # IDEA: iterate through all dictionays and change time to 0
    def refresh(self, module, submodule):
        files = glob.glob(f'{Cache_Folder}/{module}/{submodule}/*')
        for f in files:
            os.remove(f)

    def assure_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)



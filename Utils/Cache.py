import json
from time import time
import os

Cache_Folder = 'Cache'
Cache_Validity_dict = {
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
    def __init__(self, Module_Name='General', SubModule_Name='general', validity='1h'):
        self._cache_file = os.path.join(Cache_Folder, Module_Name, SubModule_Name + '.json')
        self.validity = Cache_Validity_dict[validity]
        if os.path.exists(self._cache_file):
            with open(self._cache_file, 'r', encoding='utf-8') as cache_file:
                self._cached_data = json.load(cache_file)
        else:
            path_to_cache = os.path.join(Cache_Folder, Module_Name)
            if not os.path.exists(path_to_cache):
                os.makedirs(path_to_cache)
            self._cached_data = {}

    # Adds the data to the cache with timestamp and saves it
    def save(self, identifier, data):
        identifier = str(identifier)
        self._cached_data[identifier] = {'data': data, 'time': int(time())}
        with open(self._cache_file, 'w') as file:
            json.dump(self._cached_data, file, indent=1)

    def get(self, identifier):
        identifier = str(identifier)
        if identifier in self._cached_data:
            data = self._cached_data[identifier]['data']
        else:
            data = None
        return data

    def _expired(self, identifier):
        return (time() - int(self._cached_data[identifier]['time'])) > self.validity

    def valid(self, identifier):
        identifier = str(identifier)
        return identifier in self._cached_data and not self._expired(identifier)

    # Deletes the whole cache so it gets refreshed.
    # TODO: Refresh cache in a better way, so that if api is down you can still use old cache as a fallback
    def refresh(self):
        self._cached_data = []
        with open(self._cache_file, 'w') as file:
            json.dump(self._cached_data, file, indent=1)


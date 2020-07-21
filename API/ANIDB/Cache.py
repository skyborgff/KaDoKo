from time import time
import json
import os


class Cache:
    def __init__(self, file):
        self._file = file
        self._data = {}
        if os.path.exists(self._file):
            with open(self._file, 'r') as file:
                self._data = json.load(file)

    def _expired(self, name,):
        return (time() - int(self._data[name]['time'])) > 60*60*24*30 #30 Days Cache

    def valid(self, name):
        if name in self._data and not self._expired(name):
            return True
        else:
            return False

    def get(self, name):
        return self._data[name]['data']

    def save(self, name, data):
        self._data[name] = {'data': data, 'time': int(time())}
        with open(self._file, 'w') as file:
            json.dump(self._data, file, indent=1)

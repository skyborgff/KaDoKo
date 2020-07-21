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

    def _expired(self, name, validity=60 * 60 * 2):
        return (time() - int(self._data[name]['time'])) > validity

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

    def refresh(self):
        self._data = {}
        with open(self._file, 'w') as file:
            json.dump(self._data, file, indent=1)

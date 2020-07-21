import json
import os
# http://api.anidb.net:9001/httpapi?request=anime&client=plexanidbsynchtt&clientver=1&protover=1&aid=8692
class Database:
    def __init__(self, file):
        self._file = file
        if os.path.exists(self._file):
            with open(self._file, 'r') as file:
                self.DB = json.load(file)
        else:
            self.DB = {}

    def save(self):
        with open(self._file, 'w') as file:
            json.dump(self.DB, file, indent=1)


class AnimeInfo:
    def __init__(self, Name, Season, State, Added, Type, MAL, TVDB, ANIDB):
        IDs = {'MAL': MAL, 'TVDB': TVDB, 'ANIDB': ANIDB}
        self.AnimeInfo = {
                        'Name': Name,
                        'Season': Season,
                        'State': State,
                        'Added': Added,
                        'Type': Type,
                        'IDs': IDs,
        }

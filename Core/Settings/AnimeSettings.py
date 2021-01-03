import json
import os

# Todo: implement a setting class with defaults
class AnimeSettings:
    def __init__(self):
        self.load()

    def save(self):
        settings = {'library': self.library,
                    'db': self.db,
                    'optional_libraries': self.optional_libraries,
                    'optional_dbs': self.optional_dbs,
                    'plex': self.plex,
                    'first': self.first,
                    }
        return settings

    def load(self):
        settings_file = f'Settings/Core/settings.json'
        if os.path.exists(settings_file):
            with open(settings_file) as file:
                settings = json.load(file)
                self.db = settings['db']
                self.library = settings['library']
                self.first = False
        else:
            self.first = True
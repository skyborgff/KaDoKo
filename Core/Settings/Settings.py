import json
import os


# Todo: implement a setting class with defaults
class Settings:
    def __init__(self):
        self.library: str = None
        self.db: str = None
        self.optional_libraries: list = []
        self.optional_dbs: list = []
        self.plex = False
        self.first = True
        self.load()

    def save(self):
        settings_file = f'Settings/Core/settings.json'
        settings = {'library': self.library,
                    'db': self.db,
                    'optional_libraries': self.optional_libraries,
                    'optional_dbs': self.optional_dbs,
                    'plex': self.plex,
                    'first': self.first,
                    }
        with open(settings_file, 'w+') as file:
            os.makedirs('Settings/Core', exist_ok=True)
            json.dump(settings, file, indent=4)

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
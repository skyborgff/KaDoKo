import json
import os


class Settings:
    def __init__(self):
        self.db: str = None
        self.library: str = None
        self.first = True
        self.load()

    def save(self):
        settings_file = f'Settings/Core/settings.json'
        settings = {'db': self.db,
                    'library': self.library}
        with open(settings_file, 'w+') as file:
            json.dump(settings, file, indent=1)

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

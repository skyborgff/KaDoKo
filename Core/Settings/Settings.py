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
        self.anime = self.generate_anime_settings()
        self.load()

        # Note To Self: I was going to create settings UI

    def generate_anime_settings(self):
        anime_fields = ['ageRating', 'status', 'publicRating', 'libraryStatus',
                        'personalRating', 'id', 'names', 'images', 'tags', 'soundtracks',
                        'voiceActings', 'crossRefs', 'description', 'type', 'videos',
                        'episodes', 'runnings', 'season', 'studios']

        anime_settings = {}
        anime_setting = {'language': None,
                         'provider': None}
        for field in anime_fields:
            anime_settings[field] = anime_setting
        return anime_settings


    def save(self):
        settings_file = f'Settings/Core/settings.json'
        settings = {'library': self.library,
                    'db': self.db,
                    'optional_libraries': self.optional_libraries,
                    'optional_dbs': self.optional_dbs,
                    'plex': self.plex,
                    'anime': self.anime
                    }
        with open(settings_file, 'w+') as file:
            os.makedirs('Settings/Core', exist_ok=True)
            json.dump(settings, file, indent=4)

    def load(self):
        settings_file = f'Settings/Core/settings.json'
        if os.path.exists(settings_file):
            with open(settings_file) as file:
                settings = json.load(file)
                self.db = settings.get('db', self.db)
                self.library = settings.get('library', self.library)
                self.optional_libraries = settings.get('optional_libraries', self.optional_libraries)
                self.optional_dbs = settings.get('optional_dbs', self.optional_dbs)
                self.anime = settings.get('anime', self.anime)
                self.first = False
        else:
            self.first = True
        self.save()
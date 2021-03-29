import webbrowser
from Core.Structures.Anime import Anime

class UI:
    def __init__(self, kadoko):
        self.kadoko = kadoko
        if self.first_launch():
            webbrowser.open_new_tab('http://localhost:8281/#/Setup')

    def first_launch(self):
        return self.kadoko.settings.first

    def library_list(self):
        libraries = self.kadoko.plugins.libraries()
        library_names = []
        for library in libraries:
            library_names.append(library['name'])
        return library_names

    def db_list(self):
        dbs = self.kadoko.plugins.dbs()
        dbs_names = []
        for db in dbs:
            dbs_names.append(db['name'])
        return dbs_names

    def plugin_info(self):
        plugin_info = self.kadoko.plugins.plugin_info()
        return plugin_info

    def setup_settings(self, settings: dict):
        self.kadoko.settings.library = settings.get('selected_library')
        self.kadoko.settings.db = settings.get('selected_db')
        self.kadoko.settings.optional_libraries = settings.get('optional_libraries')
        self.kadoko.settings.optional_dbs = settings.get('optional_dbs')
        self.kadoko.settings.save()

    def get_authentication_needed(self)-> dict:
        return self.kadoko.plugins.get_authentication_needed()

    def set_authentication(self, auth_data: dict):
        module_name = auth_data.get('module')
        code = auth_data.get('code')
        module = self.kadoko.plugins.get(module_name)
        module.authenticator.code(code)

    def generate_debug_graph(self, path):
        self.kadoko.database.generate_graph(path)

    def get_anime_listing(self):
        anime_hashes = self.kadoko.database.getByClass(Anime)
        listing = []
        for anime_hash in anime_hashes:
            anime = Anime.from_db(anime_hash, self.kadoko.database)
            # Todo: use the settings to request the correct localizations
            logo_url = ''
            if anime.images.list:
                logo_url = anime.images.list[0].url
            title = ''
            subtitle = ''
            if anime.names.list:
                title = anime.names.list[0].Text
                if len(anime.names.list)>1:
                    subtitle = anime.names.list[1].Text
            listing_anime = {'logo_url': logo_url,
                             'title': title,
                             'subtitle': subtitle,
                             'rating': anime.publicRating.rated,
                             'description': anime.description.Text,
                             'categories': [tag.name for tag in anime.tags.list]}
            listing.append(listing_anime)
        # Todo: add some sorting
        return listing


    def populate_tasks(self):
        self.kadoko.tasker.addCallback('library_list', self.library_list)
        self.kadoko.tasker.addCallback('db_list', self.db_list)
        self.kadoko.tasker.addCallback('plugin_info', self.plugin_info)
        self.kadoko.tasker.addCallback('setup_settings', self.setup_settings)
        self.kadoko.tasker.addCallback('get_authentication_needed', self.get_authentication_needed)
        self.kadoko.tasker.addCallback('set_authentication', self.set_authentication)
        self.kadoko.tasker.addCallback('generate_graph', self.generate_debug_graph)
        self.kadoko.tasker.addCallback('get_anime_listing', self.get_anime_listing)

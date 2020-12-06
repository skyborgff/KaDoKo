class UI:
    def __init__(self, kadoki):
        self.kadoki = kadoki

    def first_launch(self):
        return self.kadoki.settings.first

    def library_list(self):
        libraries = self.kadoki.plugins.libraries()
        library_names = []
        for library in libraries:
            library_names.append(library['name'])
        return library_names

    def db_list(self):
        dbs = self.kadoki.plugins.dbs()
        dbs_names = []
        for db in dbs:
            dbs_names.append(db['name'])
        return dbs_names

    def setup_settings(self, settings: dict):
        self.kadoki.settings.library = settings.get('selected_library')
        self.kadoki.settings.db = settings.get('selected_db')
        self.kadoki.settings.optional_libraries = settings.get('optional_libraries')
        self.kadoki.settings.optional_dbs = settings.get('optional_dbs')
        self.kadoki.settings.save()

    def get_authentication_needed(self)-> dict:
        return self.kadoki.plugins.get_authentication_needed()

    def set_authentication(self, auth_data: dict):
        module_name = auth_data.get('module')
        code = auth_data.get('code')
        module = self.kadoki.plugins.get(module_name)
        module.authenticator.code(code)

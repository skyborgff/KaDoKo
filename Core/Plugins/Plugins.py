from Core.Plugins.Loader import Loader
from Core.Plugins.Base.Auth.Authentication import AuthState

class Plugins:
    def __init__(self):
        self.list = []
        self.dictionary = {}
        self.main_library = None
        self.main_db = None

    def load(self):
        self.dictionary, self.list = Loader().get('Plugins')

    def libraries(self):
        return self.dictionary['library']

    def dbs(self):
        return self.dictionary['db']

    def get_auth_types(self):
        auth_types = []
        for plugin in self.list:
            auth_types.append(plugin.authenticator.type)

    def all_authenticated(self):
        for plugin in self.list:
            if plugin.authenticator.state == AuthState.NotLogged:
                return False
        else:
            return True


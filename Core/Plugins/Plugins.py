from Core.Plugins.Loader import Loader
from Core.Plugins.Base.Auth.Authentication import AuthState, AuthType
from Core.Plugins.Base.BaseMetadata import BaseMetadata
from Core.Plugins.Base.BaseLibrary import BaseLibrary
from typing import Union

class Plugins:
    def __init__(self, settings):
        self.list = []
        self.dictionary = {}
        self.settings = settings

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

    def get_authentication_needed(self)-> dict:
        OAuth = []
        UserPass = []
        for plugin in self.list:
            if plugin.name == self.settings.library or \
                plugin.name == self.settings.db or \
                plugin.name in self.settings.optional_libraries or \
                    plugin.name in self.settings.optional_dbs:

                if plugin.authenticator is not None and plugin.authenticator.state == AuthState.NotLogged:
                    name = plugin.name
                    logo = plugin.logo_url
                    auth_type = plugin.authenticator.type
                    if auth_type == AuthType.OAuth:
                        url = plugin.authenticator.url()
                        OAuth.append({'name': name,
                                      'url': url,
                                      'logo_url': logo,
                                      'create_url': ''})
                    elif type == AuthType.UserPass:
                        raise NotImplementedError
        return {'OAuth': OAuth, 'UserPass': UserPass}

    def get(self, name) -> Union[BaseLibrary, BaseMetadata]:
        for plugin in self.list:
            if plugin.name == name:
                return plugin
        raise ModuleNotFoundError

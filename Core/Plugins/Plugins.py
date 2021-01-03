from Core.Plugins.Loader import Loader
from Core.Plugins.Base.Auth.Authentication import AuthState, AuthType
from Core.Plugins.Base.BaseMetadata import BaseMetadata
from Core.Plugins.Base.BaseLibrary import BaseLibrary
from Core.Plugins.Base import Flags
from typing import Union, List

class Plugins:
    ''' This class handles the plugins
        A Plugin inside a the list or the dict is a dictionary with
        keys 'name' and 'module'. module houses the plugin instance '''
    def __init__(self, settings):
        # list is a list of all plugins
        self.list = []
        # plugin_ dictionary is a dictionary with the keys
        # 'library' and 'metadata' with a list of plugins each
        self.plugin_dictionary = {}
        self.settings = settings

    def load(self):
        ''' Asks the Loader to check for plugins in the "Plugins" folder '''
        self.plugin_dictionary, self.list = Loader().get('Plugins')

    def libraries(self)-> dict:
        '''Returns the library plugins'''
        return self.plugin_dictionary['library']

    def dbs(self)-> dict:
        '''Returns the library plugins'''
        return self.plugin_dictionary['metadata']

    def get_auth_types(self):
        '''Returns a list of all the authentication types of the plugins'''
        auth_types = []
        for plugin in self.list:
            auth_types.append(plugin.authenticator.type)

    def get_authentication_needed(self)-> dict:
        """ Checks if each selected library or database is not authenticated yet and returns a
        dict with a list for each authentication type (OAuth, or username and password)"""
        OAuth = []
        UserPass = []
        for plugin in self.list:
            # Select only selected plugins
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
        '''Returns the plugin instance based on name'''
        for plugin in self.list:
            if plugin.name == name:
                return plugin
        raise ModuleNotFoundError

    def meta_flagged(self, flag: Flags.MetadataFlag)-> List[BaseMetadata]:
        '''returns a list of plugins with specific metadata flags'''
        flagged = []
        for plugin in self.dbs():
            if flag in plugin.get("module").metadata_flags:
                flagged.append(plugin.get("module"))
        return flagged
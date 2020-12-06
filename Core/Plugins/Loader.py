import importlib
import pkgutil
from Core.Plugins.Base import BasePlugin, BaseLibrary, BaseMetadata
import os

class Loader:
    def __init__(self):
        self.discovered_plugins = {'library': [],
                                   'db': []}
        self.plugins = []

    def get(self, path: str):
        path_list = [f.path for f in os.scandir(os.path.abspath(path)) if f.is_dir()]
        result = pkgutil.iter_modules(path_list)
        for finder, name, ispkg in result:
            if ispkg:
                continue
            folder = os.path.basename(os.path.normpath(finder.path))
            module = importlib.import_module("Plugins." + folder + "." + name)
            Plugin = getattr(module, name)
            plugin_intance = Plugin()
            if issubclass(type(plugin_intance), BasePlugin.BasePlugin) and not ispkg:
                self.plugins.append(plugin_intance)
                print(f"Loading Plugin: {name}")
                if issubclass(type(plugin_intance), BaseLibrary.BaseLibrary):
                    self.discovered_plugins['library'].append({'name': name,
                                                               'module': plugin_intance})
                    print(f'Loaded as library')
                if issubclass(type(plugin_intance), BaseMetadata.BaseMetadata):
                    self.discovered_plugins['db'].append({'name': name,
                                                               'module': plugin_intance})
                    print(f'Loaded as metadata')

        return self.discovered_plugins, self.plugins

import importlib
import pkgutil
from Core.Plugins.Base import BasePlugin, BaseLibrary


class Loader:
    def __init__(self):
        self.discovered_plugins = {'library': [],
                                   'db': []}
        self.plugins = []

    def get(self, path: str):
        result = pkgutil.iter_modules([path])
        for finder, name, ispkg in result:
            # module = importlib.import_module("Plugins." + name)
            module = importlib.import_module("Plugins." + name)
            Plugin = getattr(module, name)
            plugin_intance = Plugin()
            if issubclass(type(plugin_intance), BasePlugin.BasePlugin) and not ispkg:
                self.plugins.append(plugin_intance)
                if issubclass(type(plugin_intance), BaseLibrary.BaseLibrary):
                    self.discovered_plugins['library'].append({'name': name,
                                                               'module': plugin_intance})
        return self.discovered_plugins, self.plugins

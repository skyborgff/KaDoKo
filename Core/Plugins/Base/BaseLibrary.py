from Core.Plugins.Base.BasePlugin import BasePlugin
from Core.Plugins.Base.Types import PluginType
from Core.Structures.List import AnimeLists


class BaseLibrary(BasePlugin):
    def __init__(self):
        super().__init__()
        self.type: PluginType = PluginType.Library

    def Lists(self)-> AnimeLists:
        raise NotImplementedError

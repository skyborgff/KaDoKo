from Core.Plugins.Base.BasePlugin import BasePlugin
from Core.Plugins.Base.Types import PluginType
from Core.Structures.List import AnimeLists
from typing import List

class BaseLibrary(BasePlugin):
    def __init__(self):
        super().__init__()
        try:
            self.type.append(PluginType.Library)
        except AttributeError:
            self.type: List[PluginType] = []

    def Lists(self)-> AnimeLists:
        raise NotImplementedError

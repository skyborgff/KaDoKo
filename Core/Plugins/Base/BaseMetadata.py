from Core.Plugins.Base.BasePlugin import BasePlugin
from Core.Plugins.Base.Types import PluginType


class BaseMetadata(BasePlugin):
    def __init__(self):
        super().__init__()
        self.type: PluginType = PluginType.Metadata

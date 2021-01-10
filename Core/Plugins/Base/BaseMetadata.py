from Core.Plugins.Base.BasePlugin import BasePlugin
from Core.Plugins.Base.Types import PluginType
import Core.Plugins.Base.Flags as Flags
from typing import List
from Core.Database.Database import Database


class BaseMetadata(BasePlugin):
    def __init__(self):
        super().__init__()
        try:
            self.type.append(PluginType.Metadata)
        except AttributeError:
            self.type: List[PluginType] = []
        self.metadata_flags: List[Flags.MetadataFlag] = []

    def PopulateAnime(self, database: Database, anime_hash: str):
        raise NotImplementedError

    def LinkIds(self, database: Database, anime_hash: str):
        pass
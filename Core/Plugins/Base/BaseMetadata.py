from Core.Plugins.Base.BasePlugin import BasePlugin
from Core.Plugins.Base.Types import PluginType
import Core.Plugins.Base.Flags as Flags
from typing import List
from Core.Database.Database import Database


class BaseMetadata(BasePlugin):
    def __init__(self):
        super().__init__()
        self.type: PluginType = PluginType.Metadata
        self.metadata_flags: List[Flags.MetadataFlag] = []

    def PopulateAnime(self, database: Database, anime_hash: str):
        raise NotImplementedError

    def LinkIds(self, database: Database, anime_hash: str):
        pass
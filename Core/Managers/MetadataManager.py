import time
from Core.Tasker.TaskManager import Tasker
from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import Core.Plugins.Base.Flags as Flags
from Core.Structures.Anime import Anime
from Core.Tasker.TaskManager import TaskImportance, TaskType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Core.kadoko import Kadoko

class MetadataManager:
    def __init__(self, kadoko: 'Kadoko'):
        self.kadoko = kadoko
        self.populate_tasks()

    def mainMetadata(self):
        return self.kadoko.plugins.get(self.kadoko.settings.db)

    def linkIds(self):
        anime_hashes = self.kadoko.database.getByClass(Anime)
        for anime_hash in anime_hashes:
            self.kadoko.tasker.addTask('linkId', TaskImportance.IMMEDIATE,
                                       TaskType.ASYNC, [anime_hash])

    def linkId(self, anime_hash):
        linkers = self.kadoko.plugins.meta_flagged(Flags.MetadataFlag.MetadataLinker)
        for linker in linkers:
            # Todo: remove self.kadoko.database argument (send just MetaIds and get them back filled)
            linker.LinkIds(self.kadoko.database, anime_hash)

    def populateAllMetadata(self):
        anime_hashes = self.kadoko.database.getByClass(Anime)
        for anime_hash in anime_hashes:
            self.kadoko.tasker.addTask('populateMetadata', TaskImportance.IMPORTANT,
                                       TaskType.ASYNC, [anime_hash])

    def populateMetadata(self, anime_hash):
        main_metadata = self.kadoko.plugins.get(self.kadoko.settings.db)
        # Todo: remove self.kadoko.database argument (send just MetaIds and get a anime struct)
        main_metadata.PopulateAnime(self.kadoko.database, anime_hash)

    def populate_tasks(self):
        self.kadoko.tasker.addCallback('linkIds', self.linkIds)
        self.kadoko.tasker.addCallback('linkId', self.linkId, max_async_calls=10)
        self.kadoko.tasker.addCallback('populateAllMetadata', self.populateAllMetadata)
        self.kadoko.tasker.addCallback('populateMetadata', self.populateMetadata, max_async_calls=20)

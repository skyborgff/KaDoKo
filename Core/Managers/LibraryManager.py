import time
from Core.Tasker.TaskManager import Tasker
from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import Core.Plugins.Base.Flags as Flags
from Core.Tasker.TaskManager import TaskImportance, TaskType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Core.kadoko import Kadoko

class LibraryManager:
    def __init__(self, kadoko: 'Kadoko'):
        self.kadoko = kadoko
        self.populate_tasks()

    def mainLibrary(self):
        return self.kadoko.plugins.get(self.kadoko.settings.library)

    def UpdateLibrary(self):
        main_list = self.mainLibrary().Lists()
        ListStruct.to_db(main_list, self.kadoko.database)
        self.kadoko.tasker.addTask('linkIds', TaskImportance.IMMEDIATE1, TaskType.SYNC)
        self.kadoko.tasker.addTask('populateAllMetadata', TaskImportance.IMMEDIATE2, TaskType.SYNC)

    def populate_tasks(self):
        # Todo: turn into a task
        self.kadoko.tasker.addCallback('UpdateLibrary', self.UpdateLibrary)

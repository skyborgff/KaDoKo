from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import Core.Plugins.Base.Flags as Flags
import time
from Core.Tasker.TaskManager import Tasker
from Core.Tasker.Tasks import populate_tasks
from Core.Managers.LibraryManager import LibraryManager
from Core.Managers.MetadataManager import MetadataManager
import asyncio

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from multiprocessing.connection import Client


class Kadoko:
    def __init__(self, taskDict: dict):
        self.tasker: Tasker = Tasker(taskDict)
        self.database: Database = Database()
        self.settings: Settings = Settings()
        self.plugins: Plugins = Plugins(self.settings)
        self.metadataManager = MetadataManager(self)
        self.libraryManager = LibraryManager(self)
        self.ui = UI(self)
        populate_tasks(self)
        asyncio.run(self.tasker.loop())

    def SettedUp(self):
        pass

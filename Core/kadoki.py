from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import Core.Plugins.Base.Flags as Flags

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from multiprocessing.connection import Client


class Kadoki:
    def __init__(self):
        self.database: Database = Database()
        self.settings: Settings = Settings()
        self.plugins: Plugins = Plugins(self.settings)
        self.plugins.load()
        self.ui = UI(self)

    def start(self):
        #Todo: get a better way of handling this
        self.UpdateLibrary()

    def SettedUp(self):
        pass

    def UpdateLibrary(self):
        main_library = self.plugins.get(self.settings.library)
        main_list = main_library.Lists()
        ListStruct.to_db(main_list, self.database)
        linkers = self.plugins.meta_flagged(Flags.MetadataFlag.MetadataLinker)
        for linker in linkers:
            linker.LinkIds(self.database)
        print('done')
        main_metadata = self.plugins.get(self.settings.db)
        main_metadata.PopulateAnime(self.database)
        # Todo: Implement Metadata Manager.
        #  He will see what are the metadata settings, and request
        #  the various metadata plugins for the correct info.
        print('done')

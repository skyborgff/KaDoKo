from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import networkx as nx
import matplotlib.pyplot as plt
import eel
from networkx_viewer import Viewer


class Kadoki:
    def __init__(self):
        self.database: Database = Database()
        self.settings: Settings = Settings()
        self.plugins: Plugins = Plugins(self.settings)
        self.plugins.load()
        self.ui = UI(self)
        self.UpdateLibrary()

    def UpdateLibrary(self):
        main_library = self.plugins.get(self.settings.library)
        main_list = main_library.Lists()
        ListStruct.convert(main_list, self.database)
        print('done')

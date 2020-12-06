from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
from Core.UI.UI import UI
import eel


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
        print(main_list)


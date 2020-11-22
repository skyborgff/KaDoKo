from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.UI.UI import UI
import eel


class Kadoki:
    def __init__(self):
        self.settings: Settings = Settings()
        self.plugins: Plugins = Plugins(self.settings)
        self.plugins.load()
        self.ui = UI(self)

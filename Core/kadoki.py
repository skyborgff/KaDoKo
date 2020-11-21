from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.UI.UI import UI
import eel


class Kadoki:
    def __init__(self):
        self.plugins = Plugins()
        self.plugins.load()
        self.settings = Settings()
        self.ui = UI(self)

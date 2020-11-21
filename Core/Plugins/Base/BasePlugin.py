from Core.Plugins.Base.Auth.Authentication import Authenticator
from Core.Plugins.Base.Types import PluginType


class BasePlugin:
    def __init__(self):
        self.name: str = None
        self.type: PluginType = None
        self.authenticator: Authenticator = None

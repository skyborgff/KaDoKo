from Core.Plugins.Base.Auth.Authentication import Authenticator
from Core.Plugins.Base.Types import PluginType
import Core.Plugins.Base.Flags as Flags
from typing import List


class BasePlugin:
    def __init__(self):
        self.name: str = None
        self.type: PluginType = None
        self.authenticator: Authenticator = None
        self.logo_url = ''
        self.call_flags: List[Flags.CallFlag] = []

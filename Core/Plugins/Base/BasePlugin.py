from Core.Plugins.Base.Auth.Authentication import Authenticator
from Core.Plugins.Base.Types import PluginType
import Core.Plugins.Base.Flags as Flags
from typing import List
from Core.Plugins.Base.Auth.NoAuth import NoAuth


class BasePlugin:
    def __init__(self):
        self.name: str = None
        self.authenticator: Authenticator = NoAuth()
        self.logo_url = ''
        self.website_url = ''
        self.create_url = ''
        self.call_flags: List[Flags.CallFlag] = []
        try:
            self.type
        except AttributeError:
            self.type: List[PluginType] = []




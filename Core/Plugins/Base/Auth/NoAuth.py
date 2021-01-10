from Core.Plugins.Base.Auth.Authentication import *


class NoAuth(Authenticator):
    def __init__(self):
        self.type = AuthType.NoAuth
        super().__init__(self.type)
        self.state = AuthState.Logged

    def login(self, username, password)-> AuthCode:
        raise NotImplementedError

from Core.Plugins.Base.Auth.Authentication import *


class UserPass(Authenticator):
    def __init__(self):
        self.type = AuthType.UserPass
        super().__init__(self.type)

    def login(self, username, password)-> AuthCode:
        raise NotImplementedError

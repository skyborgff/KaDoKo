from Core.Plugins.Base.BaseLibrary import BaseLibrary
from Core.Plugins.Base.Auth.OAuth import OAuth


class MAL(BaseLibrary):
    def __init__(self):
        super().__init__()
        self.name = "MAL"
        client_id = "add1ed488bd218c2e10146345377a0b8"
        url_auth = "https://myanimelist.net/v1/oauth2/authorize"
        url_token = "https://myanimelist.net/v1/oauth2/token"
        self.authenticator = OAuth(self.name, client_id, url_auth, url_token)

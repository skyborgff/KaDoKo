from Core.Plugins.Base.BaseMetadata import BaseMetadata
from Core.Plugins.Base.Auth.OAuth import OAuth


class Animeshon(BaseMetadata):
    def __init__(self):
        super().__init__()
        self.name = "Animeshon"
        self.logo_url = 'https://animeshon.com/e/_next/static/media/animeshon-brand.5de13d23bcab08ceaeaec5186335d368.svg'

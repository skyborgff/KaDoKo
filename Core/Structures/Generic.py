from enum import Enum
from typing import List
from collections.abc import MutableSequence
from dataclasses import dataclass, field
import pycountry
import urllib.request
from PIL import Image as PILImage
import asyncio
import random
import hashlib


@dataclass
class MetaID:
    PluginName: str
    id: str

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass()
class MetaIDs:
    list: List[MetaID] = field(default_factory=list)


@dataclass
class Localization:
    Country: str
    Language: str
    Script: str

    def __hash__(self):
        string = f"{self.Country}, {self.Language}, {self.Script}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Text:
    Text: str
    Localization: Localization

    def __hash__(self):
        string = f"{self.Text}, {self.Localization.__hash__()}"
        return hashlib.md5(string.encode()).hexdigest()



@dataclass
class Names():
    list: List[Text] = field(default_factory=list)


class Image():
    def __init__(self, url: str, height: int = None, width: int = None):
        self.url: str = url
        self.height: int = height
        self.width: int = width

        # Todo: This makes anime generation very slow.
        #  Make it only run when idle / async or something
        if False and self.height is None and self.width is None:
            self.generate_size()

    def generate_size(self):
        image = PILImage.open(urllib.request.urlopen(self.url))
        self.width, self.height = image.size

    def __hash__(self):
        string = f"{self.url}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass()
class Images():
    list: List[Image] = field(default_factory=list)





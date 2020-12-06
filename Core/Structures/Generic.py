from enum import Enum
from typing import List
from collections.abc import MutableSequence
from dataclasses import dataclass, field
#  https://pypi.org/project/pycountry/
import pycountry
import urllib.request
from PIL import Image as PILImage
import asyncio


@dataclass
class MetaID:
    PluginName: str
    id: str


@dataclass()
class MetaIDs:
    list: List[MetaID] = field(default_factory=list)


class Country(pycountry.ExistingCountries):
    pass


class Language(pycountry.Languages):
    pass


class Script(pycountry.Scripts):
    pass


@dataclass
class Localization:
    Country: Country
    Language: Language
    Script: Script


@dataclass
class Text:
    Text: str
    Localization: Localization


@dataclass
class Names():
    list: List[Text] = field(default_factory=list)


class Image:
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


@dataclass()
class Images():
    list: List[Image] = field(default_factory=list)









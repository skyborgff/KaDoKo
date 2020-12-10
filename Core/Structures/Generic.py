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
from Core.Database.Database import Database


@dataclass
class MetaID:
    PluginName: str
    id: str

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='MetaID',
                                label=f"{self.PluginName}: {self.id}", raw=self)
        return self.__hash__()

    def __hash__(self):
        string: str = str(f"{self.PluginName}{self.id}")
        return hashlib.md5(string.encode()).hexdigest()


@dataclass()
class MetaIDs:
    list: List[MetaID] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def getID(self, PluginName):
        for metaid in self.list:
            if metaid.PluginName == PluginName:
                return metaid.id
        return None

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class="MetaIDs", label=len(self.list), raw=MetaIDs())
        for metaid in self.list:
            this_hash = str(metaid.to_db(database))
            database.graph.add_edge(self.hash, this_hash)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Localization:
    Country: str = "Unknown"
    Language: str = "Unknown"
    Script: str = "Unknown"

    def __hash__(self):
        string = f"{self.Country}, {self.Language}, {self.Script}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Text:
    Text: str
    Localization: Localization = None

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Text',
                                label=f"{self.Localization.Language}: {self.Text}", raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.Text}, {self.Localization.__hash__()}"
        return hashlib.md5(string.encode()).hexdigest()



@dataclass
class Names():
    list: List[Text] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


class Image():
    # Todo: Add Large, Medium, Small to one image
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

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Image',
                                label=self.url.split("/")[-1], raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.url}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass()
class Images():
    list: List[Image] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()





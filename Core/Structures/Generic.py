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
from Core.Structures.Utils.db_functions import *


class Hashed:
    def __init__(self, *args):
        self.__post_init__()

    # def HashHash(self):
    #     # self.hash: str = self.__hash__()
    #     self.hash: str = self.__hash__()

    def __post_init__(self):
        self.Hash()

    def hashSeed(self):
        string = str(random.getrandbits(128))
        return string

    def Hash(self):
        try:
            if self.hash:
                return self.hash
        except AttributeError:
            self.hash = hashlib.md5(self.hashSeed().encode()).hexdigest()
        return self.hash

@dataclass
class MetaID(Hashed):
    PluginName: str = None
    id: str = 0

    def to_db(self, database: Database):
        # Dont look for matches. If the hash matches its the same MetaID
        return database.add_node(self, label=f"{self.PluginName}: {self.id}", raw=True)

    def hashSeed(self):
        return str(f"{self.PluginName}{self.id}")


@dataclass()
class MetaIDs(Hashed):
    list: List[MetaID] = field(default_factory=list)

    def getID(self, PluginName):
        for metaid in self.list:
            if metaid.PluginName == PluginName:
                return metaid.id
        return None

    def mappedPlugins(self):
        return [metaid.PluginName for metaid in self.list]

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for metaid in self.list:
            this_hash = metaid.to_db(database)
            database.add_edge(self.hash, this_hash)
        return self.hash

    @staticmethod
    def from_db(hash, database: Database):
        nodes = dump_info(database.graph.successors(hash), database)
        PureMetaIDs = MetaIDs()
        nodes_node, node_hash = getClass(nodes, type(MetaID()))
        PureMetaIDs.list = nodes_node
        PureMetaIDs.hash = hash
        return PureMetaIDs

@dataclass
class Localization(Hashed):
    Language: str = "Unknown"
    Script: str = "Unknown"

    def hashSeed(self):
        return f"{self.Language}{self.Script}"


@dataclass
class Text(Hashed):
    Text: str
    Localization: Localization = None

    def to_db(self, database: Database):
        return database.add_node(self, label=f"{self.Localization.Language}: {self.Text}", raw=True)


@dataclass
class Names(Hashed):
    list: List[Text] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash

@dataclass
class Image(Hashed):
    # Todo: Add Large, Medium, Small to one image.
    # Todo: hash the image itself, make url a list.
    url: str
    height: int = None
    width: int = None

    def __post_init__(self):
        super().__post_init__()
        # Todo: This makes anime generation very slow.
        #  Make it only run when idle / async or something.
        if False and self.height is None and self.width is None:
            self.generate_size()

    def generate_size(self):
        image = PILImage.open(urllib.request.urlopen(self.url))
        self.width, self.height = image.size

    def to_db(self, database: Database):
        return database.add_node(self, label=self.url.split("/")[-1], raw=True)

    def hashSeed(self):
        return f"{self.url}"


@dataclass
class Images(Hashed):
    list: List[Image] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash





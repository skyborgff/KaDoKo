from dataclasses import dataclass, field
from typing import List
from Core.Structures.Anime import Anime
from Core.Structures.Anime import convert as AnimeConvert
from Core.Database.Database import Database
import hashlib


@dataclass
class AnimeList():
        name: str
        list: List[Anime] = field(default_factory=list)

        def __hash__(self):
            string: str = str(self.name)
            return hashlib.md5(string.encode()).hexdigest()


class AnimeLists:
    def __init__(self):
        self.Watching: AnimeList = AnimeList(name="Watching")
        self.Completed: AnimeList = AnimeList(name="Completed")
        self.Hold: AnimeList = AnimeList(name="Hold")
        self.Dropped: AnimeList = AnimeList(name="Dropped")
        self.PlanToWatch: AnimeList = AnimeList(name="PlanToWatch")

    def append(self, anime: Anime):
        list_name = anime.libraryStatus.state.name
        if list_name == "Watching":
            self.Watching.list.append(anime)
        elif list_name == "Completed":
            self.Completed.list.append(anime)
        elif list_name == "Hold":
            self.Hold.list.append(anime)
        elif list_name == "Dropped":
            self.Dropped.list.append(anime)
        elif list_name == "PlanToWatch":
            self.PlanToWatch.list.append(anime)

def convert(list: AnimeLists, database: Database):
    list_hash = list.Watching.__hash__()
    database.graph.add_node(list_hash, data_class="AnimeList", label="Watching")
    for anime in list.Watching.list:
        anime_hash = AnimeConvert(anime, database)
        database.graph.add_edge(list_hash, anime_hash)

    list_hash = list.Completed.__hash__()
    database.graph.add_node(list_hash, data_class="AnimeList", label="Completed")
    for anime in list.Completed.list:
        anime_hash = AnimeConvert(anime, database)
        database.graph.add_edge(list_hash, anime_hash)

    list_hash = list.Hold.__hash__()
    database.graph.add_node(list_hash, data_class="AnimeList", label="Hold")
    for anime in list.Hold.list:
        anime_hash = AnimeConvert(anime, database)
        database.graph.add_edge(list_hash, anime_hash)

    list_hash = list.Dropped.__hash__()
    database.graph.add_node(list_hash, data_class="AnimeList", label="Dropped")
    for anime in list.Dropped.list:
        anime_hash = AnimeConvert(anime, database)
        database.graph.add_edge(list_hash, anime_hash)

    list_hash = list.PlanToWatch.__hash__()
    database.graph.add_node(list_hash, data_class="AnimeList", label="PlanToWatch")
    for anime in list.PlanToWatch.list:
        anime_hash = AnimeConvert(anime, database)
        database.graph.add_edge(list_hash, anime_hash)

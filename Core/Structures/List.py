from dataclasses import dataclass, field
from typing import List
from Core.Structures.Anime import Anime
from Core.Database.Database import Database
import hashlib
from Core.Structures.Generic import Hashed


@dataclass
class AnimeList(Hashed):
        name: str = None
        list: List[Anime] = field(default_factory=list)

        def hashSeed(self):
            return f"AnimeList{self.name}"


class AnimeLists(Hashed):
    def __init__(self):
        self.Watching: AnimeList = AnimeList(name="Watching")
        self.Completed: AnimeList = AnimeList(name="Completed")
        self.Hold: AnimeList = AnimeList(name="Hold")
        self.Dropped: AnimeList = AnimeList(name="Dropped")
        self.PlanToWatch: AnimeList = AnimeList(name="PlanToWatch")
        self.NoList: AnimeList = AnimeList(name="NoList")
        self.Hash()

    def hashSeed(self):
        return f"AnimeLists"

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
        elif list_name == "NoList":
            self.NoList.list.append(anime)


def to_db(lists: AnimeLists, database: Database):
    root_hash = database.add_node(lists, label="Root")

    list_hash = database.add_node(lists.Watching, label="Watching")
    database.add_edge(root_hash, list_hash)
    for anime in lists.Watching.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

    list_hash = database.add_node(lists.Completed, label="Completed")
    database.add_edge(root_hash, list_hash)
    for anime in lists.Completed.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

    list_hash = database.add_node(lists.Hold, label="Hold")
    database.add_edge(root_hash, list_hash)
    for anime in lists.Hold.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

    list_hash = database.add_node(lists.Dropped, label="Dropped")
    database.add_edge(root_hash, list_hash)
    for anime in lists.Dropped.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

    list_hash = database.add_node(lists.PlanToWatch, label="PlanToWatch")
    database.add_edge(root_hash, list_hash)
    for anime in lists.PlanToWatch.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

    list_hash = database.add_node(lists.NoList, label="NoList")
    database.add_edge(root_hash, list_hash)
    for anime in lists.NoList.list:
        anime_hash = anime.to_db(database)
        database.add_edge(list_hash, anime_hash)

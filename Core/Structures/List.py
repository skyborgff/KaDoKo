from dataclasses import dataclass, field
from typing import List
from Core.Structures.Anime import Anime


@dataclass
class AnimeList():
        name: str
        list: List[Anime] = field(default_factory=list)


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

from dataclasses import dataclass, field
from typing import List
from Core.Database.Database import Database

from enum import Enum
from Core.Structures.Generic import *
from Core.Structures.Other.Person import *
from datetime import datetime
import json


class ReleaseStatus(Enum):
    Unknown = 0
    Canceled = 1
    Completed = 2
    Interrupted = 3
    Ongoing = 4
    Scheduled = 5
    Suspended = 6
    WorkInProgress = 7


class RelationType(Enum):
    UNKNOWN = 0
    ADAPTATION = 1
    BASE = 2
    SAME_SETTING = 3
    ALTERNATIVE_SETTING = 4
    ALTERNATIVE_VERSION = 5
    CHARACTER = 6
    FULL_STORY = 7
    SUMMARY = 8
    PARENT_STORY = 9
    SPIN_OFF = 10
    PREQUEL = 11
    SEQUEL = 12
    MAIN_STORY = 13
    SIDE_STORY = 14
    ORIGINAL = 15
    PARODY = 16


@dataclass
class Relations:
    Type: RelationType
    # Todo: add id or something to identify


@dataclass
class AgeRating:
    Age: int
    # PG-13, R, ...
    Tag: str
    # Country the tag is valid in
    Country: str

    def convert(self, database: Database):
        database.graph.add_node(self.__hash__(),
                                raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.Age}, {self.Tag}, {self.Country}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Universe(MetaIDs):
    names: Names = field(default_factory=Names)


@dataclass
class Tag:
    name: str
    aliases: List[str] = field(default_factory=list)

    def __hash__(self):
        string = f"{self.name}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Tags():
    list: List[Tag] = field(default_factory=list)


@dataclass
class Audio:
    name: str
    link: str

    def __hash__(self):
        string = f"{self.name},{self.link}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Soundtracks():
    list: List[Audio] = field(default_factory=list)


class SongType(Enum):
    UNKNOWN = 0
    BACKGROUND = 1
    ENDING = 2
    IMAGE = 3
    INSERT = 4
    OPENING = 5
    THEME = 6


class SongVersion(Enum):
    UNKNOWN = 0
    OTHER = 1
    ENGLISH = 2
    INSTRUMENTAL = 3
    JAPANESE = 4
    MIX = 5
    NORMAL = 6
    PIANO = 7
    REMIX = 8
    TV = 9


@dataclass
class Song:
    id: str
    content: None  # Todo: Add
    audio: Audio
    type: SongType
    version: SongVersion

    def __hash__(self):
        string = f"{self.id}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class VoiceActor(Person):
    pass

@dataclass
class VoiceActors():
    list: List[VoiceActor] = field(default_factory=list)


@dataclass
class Character(Person):
    voices: VoiceActors
    names: Names
    images: Images


@dataclass
class CrossReference:
    namespace: str
    url: str
    id: str

    def __hash__(self):
        string = f"{self.namespace}, {self.url}, {self.id}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class CrossReferences():
    list: List[CrossReference] = field(default_factory=list)


class Description(str):
    pass


class AnimeType(Enum):
    UNKNOWN = 0
    OTHER = 1
    MOVIE = 2
    LIVE_ACTION = 3
    MUSIC_VIDEO = 4
    ONA = 5
    OVA = 6
    SPECIAL = 7
    TV = 8
    WEB = 9


class VideoType(Enum):
    PROMOTIONAL = 0


@dataclass
class Video:
    type: VideoType
    url: str
    width: int
    height: int
    duration: int

    def __hash__(self):
        string = f"{self.url}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Videos():
    list: List[Video] = field(default_factory=list)


class EpisodeType(Enum):
    UNKNOWN = 0
    OTHER = 1
    OPENING_ENDING = 2
    PARODY = 3
    PROMO = 4
    RECAP = 5
    REGULAR = 6
    SPECIAL = 7


@dataclass
class Episode:
    ageRating: AgeRating
    names: Names
    tags: Tags
    videos: Videos
    releaseDate: datetime
    type: EpisodeType

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Episodes():
    list: List[Episode] = field(default_factory=list)


@dataclass
class Running:
    since: datetime
    to: datetime

    def __hash__(self):
        string = f"{self.since}, {self.to}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Runnings():
    list: List[Running] = field(default_factory=list)


@dataclass
class Rating:
    rated: float = None
    rank: int = None
    popularity: int = None

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

class Seasons(Enum):
    Winter = 0
    Spring = 1
    Summer = 2
    Fall = 3


class Season(str):
    def __init__(self, Year: int = 0, SeasonName: Seasons = Seasons.Winter):
        super().__init__()
        self.Year: int = Year
        self.SeasonName: Seasons = SeasonName

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.SeasonName.name} {str(self.Year)}"


@dataclass
class Studio:
    names: Names

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Studios():
    list: List[Studio] = field(default_factory=list)


class LibraryState(Enum):
    Unknown = 0
    Watching = 1
    Completed = 2
    Hold = 3
    Dropped = 4
    PlanToWatch = 5


@dataclass
class LibraryStatus:
    state: LibraryState
    episodesWatched: int
    lastUpdated: datetime

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass(init=True, repr=True)
class Anime:
    ageRating: AgeRating = None
    status: ReleaseStatus = None
    publicRating: Rating = None
    libraryStatus: LibraryStatus = None
    personalRating: Rating = field(default_factory=Rating)
    id: MetaIDs = field(default_factory=MetaIDs)
    names: Names = field(default_factory=Names)
    images: Images = field(default_factory=Images)
    #Relations:  = : Relations
    tags: Tags = field(default_factory=Tags)
    soundtracks: Soundtracks = field(default_factory=Soundtracks)
    voiceActors: VoiceActors = field(default_factory=VoiceActors)
    crossRefs: CrossReferences = field(default_factory=CrossReferences)
    description: Description = field(default_factory=Description)
    type: AnimeType = AnimeType.UNKNOWN
    videos: Videos = field(default_factory=Videos)
    episodes: Episodes = field(default_factory=Episodes)
    runnings: Runnings = field(default_factory=Runnings)
    season: Season = field(default_factory=Season)
    studios: Studios = field(default_factory=Studios)

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


def convert(anime: Anime, database: Database):
    # Todo: maybe add Class atribute?
    hash_list = []
    if anime.ageRating:
        this_hash = str(anime.ageRating.__hash__())
        database.graph.add_node(this_hash, data=anime.ageRating)
        hash_list.append(this_hash)
    if anime.status:
        this_hash = str(anime.status.name.__hash__())
        database.graph.add_node(this_hash, data=anime.status.name)
        hash_list.append(this_hash)
    if anime.publicRating:
        this_hash = str(anime.publicRating.__hash__())
        database.graph.add_node(this_hash, data=anime.publicRating)
        hash_list.append(this_hash)
    if anime.libraryStatus:
        this_hash = str(anime.libraryStatus.__hash__())
        database.graph.add_node(this_hash, data=anime.libraryStatus)
        hash_list.append(this_hash)
    if anime.personalRating:
        this_hash = str(anime.personalRating.__hash__())
        database.graph.add_node(this_hash, data=anime.personalRating)
        hash_list.append(this_hash)
    if anime.description:
        this_hash = str(anime.description.__hash__())
        database.graph.add_node(this_hash, data=anime.description)
        hash_list.append(this_hash)
    if anime.type:
        this_hash = str(anime.type.name.__hash__())
        database.graph.add_node(this_hash, data=anime.type)
        hash_list.append(this_hash)
    if anime.season:
        this_hash = str(anime.season.__hash__())
        database.graph.add_node(this_hash, data=anime.season)
        hash_list.append(this_hash)
    for metaid in anime.id.list:
        this_hash = str(metaid.__hash__())
        database.graph.add_node(this_hash, data=metaid)
        hash_list.append(this_hash)
    for name in anime.names.list:
        this_hash = str(name.__hash__())
        database.graph.add_node(this_hash, data=name)
        hash_list.append(this_hash)
    for image in anime.images.list:
        this_hash = str(image.__hash__())
        database.graph.add_node(this_hash, data=image)
        hash_list.append(this_hash)
    for tag in anime.tags.list:
        this_hash = str(tag.__hash__())
        database.graph.add_node(this_hash, data=tag)
        hash_list.append(this_hash)
    for audio in anime.soundtracks.list:
        this_hash = str(audio.__hash__())
        database.graph.add_node(this_hash, data=audio)
        hash_list.append(this_hash)
    for voiceactor in anime.voiceActors.list:
        this_hash = str(voiceactor.__hash__())
        database.graph.add_node(this_hash, data=voiceactor)
        hash_list.append(this_hash)
    for crossref in anime.crossRefs.list:
        this_hash = str(crossref.__hash__())
        database.graph.add_node(this_hash, data=crossref)
        hash_list.append(this_hash)
    for video in anime.videos.list:
        this_hash = str(video.__hash__())
        database.graph.add_node(this_hash, data=video)
        hash_list.append(this_hash)
    for episode in anime.episodes.list:
        this_hash = str(episode.__hash__())
        database.graph.add_node(this_hash, data=episode)
        hash_list.append(this_hash)
    for running in anime.runnings.list:
        this_hash = str(running.__hash__())
        database.graph.add_node(this_hash, data=running)
        hash_list.append(this_hash)
    for studio in anime.studios.list:
        this_hash = str(studio.__hash__())
        database.graph.add_node(this_hash, data=studio)
        hash_list.append(this_hash)

    anime_hash = str(anime.__hash__())
    database.graph.add_node(anime_hash, data_class="Anime", label=anime.names.list[0].Text)
    for hash in hash_list:
        database.graph.add_edge(anime_hash, hash)

    return anime_hash

    # Note To Self: I was converting an anime to the graph.
    #  Currently it doesnt return a hash like i would like to.
    #  gotta investistigate how to achieve this.
    #  i decided to use the hash(data) as the input,
    #  and ill use node attributes to add data


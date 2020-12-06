from dataclasses import dataclass, field
from typing import List

from enum import Enum
from Core.Structures.Generic import *
from Core.Structures.Other.Person import *
from datetime import datetime


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
    Country: Country


@dataclass
class Universe(MetaIDs):
    names: Names = field(default_factory=Names)


@dataclass
class Tag:
    name: str
    aliases: List[str] = field(default_factory=list)


@dataclass
class Tags():
    list: List[Tag] = field(default_factory=list)


@dataclass
class Audio:
    name: str
    link: str


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


@dataclass
class Episodes():
    list: List[Episode] = field(default_factory=list)


@dataclass
class Running:
    since: datetime
    to: datetime


@dataclass
class Runnings():
    list: List[Running] = field(default_factory=list)


@dataclass
class Rating:
    rated: float = None
    rank: int = None
    popularity: int = None


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
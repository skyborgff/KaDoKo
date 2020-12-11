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

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='ReleaseStatus',
                                label=self.name, raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.name}"
        return str(hashlib.md5(string.encode()).hexdigest())

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
    Country: str = None

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='AgeRating',
                                label=self.Tag, raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.Age}{self.Tag}{self.Country}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Universe:
    names: Names = field(default_factory=Names)


@dataclass
class Tag:
    name: str
    aliases: List[str] = field(default_factory=list)

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Tag',
                                label=self.name, raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.name}"
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Tags():
    list: List[Tag] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Audio:
    name: str
    link: str

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Audio',
                                label=self.name, raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.name}{self.link}"
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
    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='VoiceActor',
                                label=self.name, raw=self)
        return self.__hash__()

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

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='CrossReference',
                                label=f"{self.namespace}: {self.id}", raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.namespace}{self.url}{self.id}"
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class CrossReferences():
    list: List[CrossReference] = field(default_factory=list)

@dataclass()
class Description():
    Text: str = ''
    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class='Description',
                                label="", raw=self)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()



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

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='AnimeType',
                                label=self.name, raw=self)
        return self.__hash__()


class VideoType(Enum):
    PROMOTIONAL = 0


@dataclass
class Video:
    type: VideoType
    url: str
    width: int
    height: int
    duration: int

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Video',
                                label=f"{self.url.split('/')[-1]}: {self.duration}",
                                raw=self)
        return self.__hash__()

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
    ageRating: AgeRating = None
    names: Names = None
    tags: Tags = None
    videos: Videos = None
    releaseDate: datetime = None
    type: EpisodeType = None
    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class='Episode',
                                label=f"{self.type.name}: {self.names.list[0].Text}",
                                raw=self)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Episodes:
    list: List[Episode] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class="Episodes", label=len(self.list), raw=Episodes())
        for episode in self.list:
            this_hash = str(episode.to_db(database))
            database.graph.add_edge(self.hash, this_hash)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Running:
    since: datetime
    to: datetime

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        since = to = "Unknown"
        if self.since:
            since = self.since.isoformat()
        if self.to:
            to = self.to.isoformat()
        label = f"from:{since} to:{to}"
        database.graph.add_node(self.__hash__(), data_class='Running',
                                label=label,
                                raw=self)
        return self.__hash__()

    def __hash__(self):
        string = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

@dataclass
class Runnings():
    list: List[Running] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Rating:
    rated: float = None
    rank: int = None
    popularity: int = None

    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class='Rating',
                                label=f"{self.rated}/{self.rank}/{self.popularity}",
                                raw=self)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

class Seasons(Enum):
    Unknown = 0
    Winter = 1
    Spring = 2
    Summer = 3
    Fall = 4


class Season:
    def __init__(self, Year: int = 0, SeasonName: Seasons = Seasons.Unknown):
        super().__init__()
        self.Year: int = Year
        self.SeasonName: Seasons = SeasonName

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Season',
                                label=str(self), raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{str(self)}"
        return hashlib.md5(string.encode()).hexdigest()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.SeasonName.name} {str(self.Year)}"


@dataclass
class Studio:
    names: Names
    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class='Studio',
                                label=self.names.list[0].Text, raw=self)
        return self.hash

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


@dataclass
class Studios():
    list: List[Studio] = field(default_factory=list)
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()

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
    episodesWatched: int = 0
    lastUpdated: datetime = datetime.utcfromtimestamp(0.)
    def __post_init__(self):
        self.hash = self.__hash__()

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.hash, data_class='LibraryStatus',
                                label=f"{self.state.name}/{self.episodesWatched}",
                                raw=self)
        return self.hash

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
    def __post_init__(self):
        self.hash = self.__hash__()

    def __hash__(self):
        string: str = str(random.getrandbits(128))
        return hashlib.md5(string.encode()).hexdigest()


    def to_db(self, database: Database):
        # Todo: maybe add Class atribute?
        # Todo: When adding to the database see if another exists
        #  see the diferences (like going from scheduled to airing)
        #  and call the appropriate flags
        hash_list: List[str] = []
    
        if self.ageRating:
            this_hash = self.ageRating.to_db(database)
            hash_list.append(this_hash)
    
        if self.status:
            this_hash = str(self.status.to_db(database))
            hash_list.append(this_hash)
    
        if self.publicRating:
            this_hash = str(self.publicRating.to_db(database))
            hash_list.append(this_hash)
    
        if self.libraryStatus:
            this_hash = str(self.libraryStatus.to_db(database))
            hash_list.append(this_hash)
    
        if self.personalRating:
            this_hash = str(self.personalRating.to_db(database))
            hash_list.append(this_hash)
    
        if self.description:
            this_hash = str(self.description.to_db(database))
            hash_list.append(this_hash)
    
        if self.type:
            this_hash = self.type.to_db(database)
            hash_list.append(this_hash)
    
        if self.season:
            this_hash = str(self.season.to_db(database))
            hash_list.append(this_hash)

        if self.episodes:
            this_hash = str(self.episodes.to_db(database))
            hash_list.append(this_hash)
    
        if self.id:
            this_hash = str(self.id.to_db(database))
            hash_list.append(this_hash)
    
        for name in self.names.list:
            this_hash = str(name.to_db(database))
            hash_list.append(this_hash)
    
        for image in self.images.list:
            this_hash = str(image.to_db(database))
            hash_list.append(this_hash)
    
        for tag in self.tags.list:
            this_hash = str(tag.to_db(database))
            hash_list.append(this_hash)
    
        for audio in self.soundtracks.list:
            this_hash = str(audio.to_db(database))
            hash_list.append(this_hash)
    
        for voiceactor in self.voiceActors.list:
            this_hash = str(voiceactor.to_db(database))
            hash_list.append(this_hash)
    
        for crossref in self.crossRefs.list:
            this_hash = str(crossref.to_db(database))
            hash_list.append(this_hash)
    
        for video in self.videos.list:
            this_hash = str(video.to_db(database))
            hash_list.append(this_hash)
    
        for running in self.runnings.list:
            this_hash = str(running.to_db(database))
            hash_list.append(this_hash)
    
        for studio in self.studios.list:
            this_hash = str(studio.to_db(database))
            hash_list.append(this_hash)

        database.graph.add_node(self.hash, data_class="Anime", label=self.names.list[0].Text)
        for hash in hash_list:
            database.graph.add_edge(self.hash, hash)
    
        return self.hash

def from_db(node_hash: str, database: Database)-> Anime:
    anime_node = database.graph.nodes[node_hash]
    info_nodes = database.graph.successors(node_hash)

    def getClass(node_list, check_class):
        matches = []
        node_matches = []
        for node in node_list:
            info = node["info"]["raw"]
            if type(info) == check_class:
                matches.append(info)
                node_matches.append(node["hash"])
        return matches, node_matches

    def dump_info(node_hashes):
        info_dump = []
        for hash in node_hashes:
            info = database.graph.nodes[hash]
            info_dump.append({"info": info, "hash": hash})
        return info_dump

    info_dump = dump_info(info_nodes)


    PureAnime = Anime()
    PureAnime.hash = node_hash

    ageRating, node_hash = getClass(info_dump, AgeRating)
    if ageRating:
        PureAnime.ageRating = ageRating[0]
    status, node_hash = getClass(info_dump, ReleaseStatus)
    if status:
        PureAnime.status = status[0]
    publicRating, node_hash = getClass(info_dump, Rating)
    if publicRating:
        PureAnime.publicRating = publicRating[0]
    libraryStatus, node_hash = getClass(info_dump, LibraryStatus)
    if libraryStatus:
        PureAnime.libraryStatus = libraryStatus[0]
    personalRating, node_hash = getClass(info_dump, Rating)
    if personalRating:
        PureAnime.personalRating = personalRating[0]
    description, node_hash = getClass(info_dump, Description)
    if description:
        PureAnime.description = description[0]
    animeType, node_hash = getClass(info_dump, AnimeType)
    if animeType:
        PureAnime.type = animeType[0]
    season = getClass(info_dump, Season)
    if season:
        PureAnime.season = season

    metaids, node_hash = getClass(info_dump, MetaIDs)
    if node_hash:
        node_hashes = database.graph.successors(node_hash[0])
        nodes = dump_info(node_hashes)
        metaid, node_hash2 = getClass(nodes, MetaID)
        PureAnime.id = MetaIDs()
        # setting the hash so info doesnt repeat
        PureAnime.id.hash = node_hash[0]
        PureAnime.id.list = metaid

    episodes, node_hash = getClass(info_dump, Episodes)
    if node_hash:
        node_hashes = database.graph.successors(node_hash[0])
        nodes = dump_info(node_hashes)
        episode, node_hash2 = getClass(nodes, MetaID)
        PureAnime.episodes = Episodes()
        # setting the hash so info doesnt repeat
        PureAnime.episodes.hash = node_hash[0]
        PureAnime.episodes.list = episode


    # Todo: Text is not OK!
    # name = getClass(info_dump, MetaID)
    # if name:
    #     PureAnime.names.list = name
    # image = getClass(info_dump, MetaID)
    # if image:
    #     PureAnime.images.list = image
    # tag = getClass(info_dump, MetaID)
    # if tag:
    #     PureAnime.tags.list = tag
    # audio = getClass(info_dump, MetaID)
    # if audio:
    #     PureAnime.soundtracks.list = audio
    # voiceactor = getClass(info_dump, MetaID)
    # if voiceactor:
    #     PureAnime.voiceActors.list = voiceactor
    # crossref = getClass(info_dump, MetaID)
    # if crossref:
    #     PureAnime.crossRefs.list = crossref
    # video = getClass(info_dump, MetaID)
    # if video:
    #     PureAnime.videos.list = video

    return PureAnime

    # Note To Self: I was separating each conversion
    #  into each class
    # Note To Self: Next task after that is to get the full anime info after this.


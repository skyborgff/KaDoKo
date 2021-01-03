from dataclasses import dataclass, field
from typing import List
from Core.Database.Database import Database

from enum import Enum
from Core.Structures.Generic import *
from Core.Structures.Other.Person import *
from datetime import datetime
import json
from Core.Structures.Utils.db_functions import *


class ReleaseStatus(Hashed, Enum):
    UNKNOWN = 0
    CANCELED = 1
    COMPLETED = 2
    INTERRUPTED = 3
    ONGOING = 4
    SCHEDULED = 5
    SUSPENDED = 6
    WORKINPROGRESS = 7

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"


class RelationType(Hashed, Enum):
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

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"


@dataclass
class Relation(Hashed):
    MetaIDs: MetaIDs
    Type: RelationType = RelationType.UNKNOWN

    def to_db(self, database: Database):
        database.add_node(self, label=self.Type.name)
        typehash = self.Type.to_db(database)
        database.add_edge(self.hash, typehash)
        metahash = self.MetaIDs.to_db(database)
        database.add_edge(self.hash, metahash)
        return self.hash


@dataclass
class Relations(Hashed):
    list: List[Relation] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


@dataclass
class AgeRating(Hashed):
    Age: int = 0
    # PG-13, R, ...
    Tag: str = ''
    # Country the tag is valid in
    Country: str = ''

    def to_db(self, database: Database):
        return database.add_node(self, label=self.Tag, raw=True)

    def hashSeed(self):
        return f"{self.Age}{self.Tag}{self.Country}"


@dataclass
class Universe(Hashed):
    names: Names = field(default_factory=Names)

    def to_db(self, database: Database):
        database.add_node(self, label="", raw=True)
        namehash = self.names.to_db(database)
        database.add_edge(self.hash, namehash)
        return self.hash


@dataclass
class Tag(Hashed):
    name: str
    aliases: List[str] = field(default_factory=list)

    def to_db(self, database: Database):
        # Todo: See if there are more Tags in the database with the same name
        #  but that may have a different list of aliases
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}"


@dataclass
class Tags(Hashed):
    list: List[Tag] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


@dataclass
class Audio(Hashed):
    name: str
    link: str

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{self.link}"


@dataclass
class Soundtracks(Hashed):
    list: List[Audio] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


class SongType(Hashed, Enum):
    UNKNOWN = 0
    BACKGROUND = 1
    ENDING = 2
    IMAGE = 3
    INSERT = 4
    OPENING = 5
    THEME = 6

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"


class SongVersion(Hashed, Enum):
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

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"


@dataclass
class Song(Hashed):
    content: None  # Todo: Add
    audio: Audio
    type: SongType
    version: SongVersion

    def to_db(self, database: Database):
        database.add_node(self, label='')
        # contenthash = self.content.to_db(database)
        # database.add_edge(self.hash, contenthash)
        audiohash = self.audio.to_db(database)
        database.add_edge(self.hash, audiohash)
        typehash = self.type.to_db(database)
        database.add_edge(self.hash, typehash)
        versionhash = self.version.to_db(database)
        database.add_edge(self.hash, versionhash)
        return self.hash


@dataclass
class Character(Person, Hashed):
    names: Names
    images: Images

    def to_db(self, database: Database):
        database.add_node(self, label=self.name, raw=True)
        database.add_edge(self.hash, self.names.to_db(database))
        database.add_edge(self.hash, self.images.to_db(database))
        return self.hash


@dataclass
class VoiceActing(Hashed):
    actor: Person = None
    voiced: Character = None

    def to_db(self, database: Database):
        database.add_node(self, label=self.actor.name)
        if self.actor:
            database.add_edge(self.hash, self.actor.to_db(database))
        if self.voiced:
            database.add_edge(self.hash, self.voiced.to_db(database))
        return self.hash


@dataclass
class VoiceActings(Hashed):
    list: List[VoiceActing] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


@dataclass
class CrossReference(Hashed):
    namespace: str
    url: str
    id: str

    def to_db(self, database: Database):
        database.add_node(self, label=f"{self.namespace}: {self.id}", raw=True)
        return self.__hash__()

    def hashSeed(self):
        return f"{self.namespace}{self.url}{self.id}"

class CastingType(Hashed, Enum):
    UNKNOWN = 0
    MAIN = 1
    SUPPORT = 2
    APPEARS = 3

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"

@dataclass
class Starring(Hashed):
    character: Character
    type: CastingType


@dataclass
class CrossReferences(Hashed):
    list: List[CrossReference] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self, item_hash)
        return self.hash


@dataclass()
class Description(Hashed):
    Text: str = ''

    def to_db(self, database: Database):
        return database.add_node(self, label="", raw=True)


class AnimeType(Hashed, Enum):
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
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}"


class VideoType(Hashed, Enum):
    UNKNOWN = 0
    PROMOTIONAL = 1

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}"


@dataclass
class Video(Hashed):
    url: str
    type: VideoType = VideoType.UNKNOWN
    width: int = None
    height: int = None
    duration: int = None

    def to_db(self, database: Database):
        database.add_node(self, label=f"{self.url.split('/')[-1]}: {self.duration}", raw=True)
        database.add_edge(self.hash, self.type.to_db(database))
        return self.hash

    def hashSeed(self):
        return f"{self.url}"


@dataclass
class Videos(Hashed):
    list: List[Video] = field(default_factory=list)

    def to_db(self, database: Database):
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


class EpisodeType(Hashed, Enum):
    UNKNOWN = 0
    OTHER = 1
    OPENING_ENDING = 2
    PARODY = 3
    PROMO = 4
    RECAP = 5
    REGULAR = 6
    SPECIAL = 7

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}"


@dataclass
class Episode(Hashed):
    ageRating: AgeRating = None
    names: Names = None
    tags: Tags = None
    videos: Videos = None
    type: EpisodeType = EpisodeType.UNKNOWN
    releaseDate: datetime = None
    index: str = '0'
    description: Description = None

    def to_db(self, database: Database):
        database.add_node(self, label=self.index, raw=True)
        if self.ageRating:
            database.add_edge(self.hash, self.ageRating.to_db(database))
        if self.names:
            database.add_edge(self.hash, self.names.to_db(database))
        if self.tags:
            database.add_edge(self.hash, self.tags.to_db(database))
        if self.videos:
            database.add_edge(self.hash, self.videos.to_db(database))
        if self.type:
            database.add_edge(self.hash, self.type.to_db(database))
        if self.description:
            database.add_edge(self.hash, self.description.to_db(database))
        return self.hash

    @staticmethod
    def from_db(hash, database: Database):
        node = database.graph.nodes[hash]
        nodes = dump_info(database.graph.successors(hash), database)
        PureEpisode = Episode()
        PureEpisode.ageRating = getClass(nodes, AgeRating)[0][0]
        PureEpisode.names = getClass(nodes, Names)[0][0]
        PureEpisode.tags = getClass(nodes, Tags)[0][0]
        PureEpisode.videos = getClass(nodes, Videos)[0][0]
        PureEpisode.type = getClass(nodes, EpisodeType)[0][0]
        PureEpisode.releaseDate = node.releaseDate
        PureEpisode.index = node.index
        PureEpisode.hash = hash
        return PureEpisode

@dataclass
class Episodes(Hashed):
    list: List[Episode] = field(default_factory=list)

    def to_db(self, database: Database):
        self.list.sort(key=lambda e: e.index)
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash

    @staticmethod
    def from_db(hash, database: Database):
        nodes = dump_info(database.graph.successors(hash), database)
        PureEpisodes = Episodes()
        for episode, hash in getClass(nodes, Episode):
            PureEpisodes.list.append(episode.from_db(hash, database))
        PureEpisodes.hash = hash
        return PureEpisodes

@dataclass
class Running(Hashed):
    since: datetime
    to: datetime

    def to_db(self, database: Database):
        since = to = "Unknown"
        if self.since:
            since = self.since.isoformat()
        if self.to:
            to = self.to.isoformat()
        label = f"from:{since} to:{to}"
        return database.add_node(self, label=label, raw=True)


@dataclass
class Runnings(Hashed):
    list: List[Running] = field(default_factory=list)

    def to_db(self, database: Database):
        self.list.sort(key=lambda e: e.index)
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


@dataclass
class Rating(Hashed):
    rated: float = None
    rank: int = None
    popularity: int = None

    def to_db(self, database: Database):
        database.add_node(self, label=f"{self.rated}/{self.rank}/{self.popularity}", raw=True)
        return self.hash


class Seasons(Hashed, Enum):
    Unknown = 0
    Winter = 1
    Spring = 2
    Summer = 3
    Fall = 4

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}"


@dataclass
class Year(Hashed):
    number: int = 0

    def to_db(self, database: Database):
        return database.add_node(self, label=str(self.number), raw=True)

    def hashSeed(self):
        return f"{self.number}"


@dataclass
class Season(Hashed):
    Year: Year = Year(0)
    SeasonName: Seasons = Seasons.Unknown

    def to_db(self, database: Database):
        database.add_node(self, label=str(self))
        database.add_edge(self.hash, self.Year.to_db(database))
        database.add_edge(self.hash, self.SeasonName.to_db(database))
        return self.hash

    def hashSeed(self):
        return f"{str(self.Year.number)}{self.SeasonName.name}"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.SeasonName.name} {str(self.Year)}"

    @staticmethod
    def from_db(hash, database: Database):
        nodes = dump_info(database.graph.successors(hash), database)
        PureSeason = Season()
        PureSeason.SeasonName = simpleAdd(PureSeason.SeasonName, nodes)
        PureSeason.Year = simpleAdd(PureSeason.Year, nodes)
        return PureSeason

@dataclass
class Studio(Hashed):
    names: Names = field(default_factory=Names)

    def to_db(self, database: Database):
        database.add_node(self, label='')
        database.add_edge(self.hash, self.names.to_db(database))
        return self.hash


@dataclass
class Studios(Hashed):
    list: List[Studio] = field(default_factory=list)

    def to_db(self, database: Database):
        self.list.sort(key=lambda e: e.index)
        database.add_node(self, label=str(len(self.list)))
        for item in self.list:
            item_hash = item.to_db(database)
            database.add_edge(self.hash, item_hash)
        return self.hash


class LibraryState(Enum):
    Unknown = 0
    Watching = 1
    Completed = 2
    Hold = 3
    Dropped = 4
    PlanToWatch = 5


@dataclass
class LibraryStatus(Hashed):
    state: LibraryState = LibraryState.Unknown
    episodesWatched: int = 0
    lastUpdated: datetime = datetime.utcfromtimestamp(0.)

    def to_db(self, database: Database):
        database.add_node(self, label=f"{self.state.name}/{self.episodesWatched}", raw=True)
        return self.hash


@dataclass(init=True, repr=True)
class Anime(Hashed):
    ageRating: AgeRating = field(default_factory=AgeRating)
    status: ReleaseStatus = ReleaseStatus.UNKNOWN
    publicRating: Rating = field(default_factory=Rating)
    libraryStatus: LibraryStatus = field(default_factory=LibraryStatus)
    personalRating: Rating = field(default_factory=Rating)
    id: MetaIDs = field(default_factory=MetaIDs)
    names: Names = field(default_factory=Names)
    images: Images = field(default_factory=Images)
    # Relations:  = : Relations
    tags: Tags = field(default_factory=Tags)
    soundtracks: Soundtracks = field(default_factory=Soundtracks)
    voiceActings: VoiceActings = field(default_factory=VoiceActings)
    crossRefs: CrossReferences = field(default_factory=CrossReferences)
    description: Description = field(default_factory=Description)
    type: AnimeType = AnimeType.UNKNOWN
    videos: Videos = field(default_factory=Videos)
    episodes: Episodes = field(default_factory=Episodes)
    runnings: Runnings = field(default_factory=Runnings)
    season: Season = field(default_factory=Season)
    studios: Studios = field(default_factory=Studios)

    # Todo: add characters (starring, character and relation)

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
            this_hash = self.status.to_db(database)
            hash_list.append(this_hash)
    
        if self.publicRating:
            this_hash = self.publicRating.to_db(database)
            hash_list.append(this_hash)
    
        if self.libraryStatus:
            this_hash = self.libraryStatus.to_db(database)
            hash_list.append(this_hash)
    
        if self.personalRating:
            this_hash = self.personalRating.to_db(database)
            hash_list.append(this_hash)
    
        if self.description:
            this_hash = self.description.to_db(database)
            hash_list.append(this_hash)
    
        if self.type:
            this_hash = self.type.to_db(database)
            hash_list.append(this_hash)
    
        if self.season:
            this_hash = self.season.to_db(database)
            hash_list.append(this_hash)

        if self.episodes:
            this_hash = self.episodes.to_db(database)
            hash_list.append(this_hash)
    
        if self.id:
            this_hash = self.id.to_db(database)
            hash_list.append(this_hash)
    
        for name in self.names.list:
            this_hash = name.to_db(database)
            hash_list.append(this_hash)
    
        for image in self.images.list:
            this_hash = image.to_db(database)
            hash_list.append(this_hash)
    
        for tag in self.tags.list:
            this_hash = tag.to_db(database)
            hash_list.append(this_hash)
    
        for audio in self.soundtracks.list:
            this_hash = audio.to_db(database)
            hash_list.append(this_hash)
    
        for voiceacting in self.voiceActings.list:
            this_hash = voiceacting.to_db(database)
            hash_list.append(this_hash)
    
        for crossref in self.crossRefs.list:
            this_hash = crossref.to_db(database)
            hash_list.append(this_hash)
    
        for video in self.videos.list:
            this_hash = video.to_db(database)
            hash_list.append(this_hash)
    
        for running in self.runnings.list:
            this_hash = running.to_db(database)
            hash_list.append(this_hash)
    
        for studio in self.studios.list:
            this_hash = studio.to_db(database)
            hash_list.append(this_hash)

        database.add_node(self, label=self.names.list[0].Text)
        for hash in hash_list:
            database.add_edge(self.hash, hash)
        return self.hash

    @staticmethod
    def from_db(hash: str, database: Database):
        """Generates an Anime structure from the database starting from an anime node"""
        successors_hashes = database.graph.successors(hash)
        PureAnime = Anime()
        PureAnime.hash = hash

        nodes_info = dump_info(successors_hashes, database)

        PureAnime.ageRating = simpleAdd(PureAnime.ageRating, nodes_info)
        PureAnime.status = simpleAdd(PureAnime.status, nodes_info)
        PureAnime.publicRating = simpleAdd(PureAnime.publicRating, nodes_info)
        PureAnime.libraryStatus = simpleAdd(PureAnime.libraryStatus, nodes_info)
        PureAnime.personalRating = simpleAdd(PureAnime.personalRating, nodes_info)
        PureAnime.description = simpleAdd(PureAnime.description, nodes_info)
        PureAnime.type = simpleAdd(PureAnime.type, nodes_info)

        season, node_hash = getClass(nodes_info, Season)
        if season:
            PureAnime.season = Season.from_db(node_hash[0], database)

        metaids, node_hash = getClass(nodes_info, MetaIDs)
        if metaids:
            PureAnime.id = MetaIDs.from_db(node_hash[0], database)

        episodes, node_hash = getClass(nodes_info, Episodes)
        if episodes:
            if episodes[0].list:
                PureAnime.episodes = Episodes.from_db(node_hash[0], database)


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

from Core.Structures.Generic import *
from dataclasses import dataclass


class Gender(Enum):
    UNKNOWN = 0
    UNDEFINED = 1
    OTHER = 2
    FEMALE = 3
    FEMALE_TRAP = 4
    HERMAPHRODITIC = 5
    INTERSEXUAL = 6
    MALE = 7
    MALE_TRAP = 8


@dataclass
class Person():
    MetaIDs: MetaIDs
    name: str
    birthday: str
    gender: Gender
    country: str

    def to_db(self, database: Database):
        # No need to look for matches, as if the hash matches,
        # it means its the same AgeRating
        database.graph.add_node(self.__hash__(), data_class='Person',
                                label=self.name, raw=self)
        return self.__hash__()

    def __hash__(self):
        string = f"{self.name}"
        return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

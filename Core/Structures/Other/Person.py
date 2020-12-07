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

    def __hash__(self):
        string = f"{self.name}, {self.birthday}"
        return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

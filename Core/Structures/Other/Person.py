from Core.Structures.Generic import *
from dataclasses import dataclass


class Gender(Hashed, Enum):
    UNKNOWN = 0
    UNDEFINED = 1
    OTHER = 2
    FEMALE = 3
    FEMALE_TRAP = 4
    HERMAPHRODITIC = 5
    INTERSEXUAL = 6
    MALE = 7
    MALE_TRAP = 8

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"


@dataclass
class Person(Hashed):
    name: str
    birthday: str
    gender: Gender
    country: str
    age: int

    def to_db(self, database: Database):
        return database.add_node(self, label=self.name, raw=True)

    def hashSeed(self):
        return f"{self.name}{type(self).__name__}"

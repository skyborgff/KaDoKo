import json
import jsonpickle
from json import JSONEncoder

class Ids:
    def __init__(self):
        self.anidb = None
        self.mal = None

class AnimeSeason:
    def __init__(self):
        self.id = Ids()
        # ["Watching", "PTW", "Dropped", "Completed"]
        self.ListType = None

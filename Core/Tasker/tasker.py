from enum import Enum
from typing import List

class taskType(Enum):
    IMMEDIATE = 0
    IDLE = 1

class runType(Enum):
    SYNC = 0
    ASYNC = 1

class task:
    def __init__(self, function,
                 taskType: taskType = taskType.IMMEDIATE,
                 runType: runType = runType.SYNC):
        function = function
        taskType: taskType = taskType
        runType: runType = runType

class tasker:
    def __init__(self):
        self.tasklist: List[task] = []

    def add(self, task: task):
        self.tasklist.append(task)


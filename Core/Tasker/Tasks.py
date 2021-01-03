from Core.Plugins.Plugins import Plugins
from Core.Settings.Settings import Settings
from Core.Database.Database import Database
import Core.Structures.List as ListStruct
from Core.UI.UI import UI
import Core.Plugins.Base.Flags as Flags
from Core.Tasker.TaskManager import TaskImportance, TaskType

import time
from Core.Tasker.TaskManager import Tasker

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Core.kadoko import Kadoko


def populate_tasks(kadoko: 'Kadoko'):
    kadoko.plugins.load()
    kadoko.ui.populate_tasks()
    kadoko.tasker.addTask('UpdateLibrary', TaskImportance.IMMEDIATE, TaskType.SYNC)

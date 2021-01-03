from typing import List
import random
import string
import time
import logging
log = logging.getLogger(__name__)
from enum import Enum
import threading
import concurrent.futures

class TaskImportance(Enum):
    UI = 0
    IMMEDIATE = 10
    IMMEDIATE1 = 11
    IMMEDIATE2 = 12
    IMMEDIATE3 = 13
    IMPORTANT = 20
    IMPORTANT1 = 21
    IMPORTANT2 = 22
    IDLE = 30


class TaskType(Enum):
    THREAD = 0
    ASYNC = 1
    SYNC = 2

MAX_ASYNC_TASKS = 10


class Tasker():
    def __init__(self, taskDict: dict):
        self._taskDict = taskDict
        self._tasksCallback: dict = {}
        self._last_task_time = 0

    def addCallback(self, name: str, function: callable, max_async_calls: int = 1):
        '''Add the function to the functions list with a name assigned so it can be called later'''
        self._tasksCallback[name] = {'callback': function, 'max_async_calls': max_async_calls}

    def addTask(self, task_name: str, importance: TaskImportance = TaskImportance.IDLE,
                task_type: TaskType = TaskType.SYNC, args: List[str] = None):
        '''Add a task to the task queue'''
        if args is None:
            args = []
        task, code = self._createTask(task_name, importance, task_type, args)
        self._taskDict['tasks'] += [task]
        return code

    def getReply(self, code) -> str:
        '''Waits for the a reply with a given code and returns it'''
        reply = self._checkReply(code)
        while reply is None:
            time.sleep(0.1)
            reply = self._checkReply(code)
        return reply

    def addWaitReply(self, task_name: str, importance: TaskImportance = TaskImportance.IDLE,
                     task_type: TaskType = TaskType.SYNC, args: List[str] = None):
        '''Add a task to the task queue and wait for it to reply'''
        if args is None:
            args = []
        code = self.addTask(task_name, importance, task_type, args)
        return self.getReply(code)

    def _checkReply(self, code):
        '''Delete the reply if it exists, and returns it'''
        real_reply = None
        for index in range(len(self._taskDict['replies'])):
            if self._taskDict['replies'][index]['code'] == code:
                real_reply = self._taskDict['replies']['result']
                self._taskDict['replies'].pop(index)
                continue
        return real_reply

    @staticmethod
    def _generateTaskCode():
        '''Generate random task code to identify them'''
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for _ in range(12))
        return result_str

    def _createTask(self, task_name: str, importance: TaskImportance = TaskImportance.IDLE,
                    task_type: TaskType = TaskType.SYNC, args: List[str] = None):
        if args is None:
            args = []
        task_code = self._generateTaskCode()
        task_dict = {'name': task_name,
                     'args': args,
                     'code': task_code,
                     'task_importance': importance.name,
                     'task_type': task_type.name}
        return task_dict, task_code

    def _getTasks(self, filter=None) -> (list, dict):
        if filter:
            current_tasks = [task for task in self._taskDict.get('tasks')
                             if TaskImportance[task.get('task_importance')] == filter]
        else:
            current_tasks = [task for task in self._taskDict.get('tasks')]
        current_tasks.sort(key=lambda t: TaskImportance[t.get('task_importance')].value)

        current_tasks_dict = {TaskImportance[importance]:
                                  {TaskType[task_type]:
                                       {task.get('name'): []
                                        for task in current_tasks if task.get('task_type') == task_type and task.get('task_importance') == importance}
                                   for task_type in list(TaskType.__members__)}
                              for importance in list(TaskImportance.__members__)}

        for task in current_tasks:
            task_name = task.get('name')
            task_importance = TaskImportance[task.get('task_importance')]
            task_type = TaskType[task.get('task_type')]
            current_tasks_dict.get(task_importance).get(task_type).get(task_name).append(task)

        return current_tasks, current_tasks_dict

    def _completeTask(self, code, reply):
        current_tasks, current_tasks_dict = self._getTasks()
        for index, item in enumerate(current_tasks):
            if item['code'] == code:
                current_tasks.pop(index)
                continue
        self._taskDict['tasks'] = current_tasks
        self._taskDict['replies'] += [{'code': code, 'reply': reply}]

    def __run(self, task):
        task_name = task.get('name')
        task_args = task.get('args')
        task_code = task.get('code')
        task_importance = TaskImportance[task.get('task_importance')]
        task_type = TaskType[task.get('task_type')]

        callback = self._tasksCallback.get(task_name)
        if not callback:
            print(f'Task "{task_name}" - "{task_code}" has no callback created')
            return
        callback = callback.get('callback')
        # print(f'Running Task {task_type.name}: "{task_name}" - "{task_code}"')
        if task_type == TaskType.SYNC:
            reply = callback(*task_args)
        elif task_type == TaskType.ASYNC:
            thread = threading.Thread(target=callback, args=task_args)
            thread.start()
            reply = thread.join()
            # raise NotImplementedError
        elif task_type == TaskType.THREAD:
            raise NotImplementedError
        else:
            raise NotImplementedError
        # print(f'Completed Task {task_type.name}: "{task_name}" - "{task_code}"')
        self._completeTask(task_code, reply)
        self._last_task_time = time.time()
        return

    def _runTasks(self, current_tasks: list, current_tasks_dict: dict):
        for importance in list(TaskImportance.__members__):
            importance_enum = TaskImportance[importance]
            importance_tasks = current_tasks_dict[importance_enum]
            if importance_tasks.get(TaskType.THREAD):
                raise NotImplementedError
            elif importance_tasks.get(TaskType.ASYNC):
                tasks = importance_tasks.get(TaskType.ASYNC)
                for task_name in tasks:
                    callback = self._tasksCallback.get(task_name)
                    if not callback:
                        print(f'Task "{task_name}" has no callback created')
                        return
                    max_async_calls = callback.get('max_async_calls')
                    next_tasks = tasks[task_name]
                    called = 0
                    async_tasks = []
                    for task in next_tasks:
                        if called < max_async_calls:
                            called += 1
                            async_tasks.append(task)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        executor.map(self.__run, async_tasks)
                        return
            elif importance_tasks.get(TaskType.SYNC):
                tasks = importance_tasks.get(TaskType.SYNC)
                for task_name in tasks:
                    self.__run(tasks[task_name][0])
                    return

    def sleep_calculator(self, current_tasks):
        sleep = 1
        time_since_last = time.time() - self._last_task_time
        if len(current_tasks) != 0:
            next_task = current_tasks[0]
            if TaskImportance[next_task.get('task_importance')].value < TaskImportance.IDLE.value:
                sleep = 0
        return sleep

    def UIloop(self):
        while True:
                current_tasks, current_tasks_dict = self._getTasks(filter=TaskImportance.UI)
                self._runTasks(current_tasks, current_tasks_dict)
                time.sleep(self.sleep_calculator(self._getTasks(filter=TaskImportance.UI)[0]))

    def normalloop(self):
        while True:
                current_tasks, current_tasks_dict = self._getTasks(filter=None)
                self._runTasks(current_tasks, current_tasks_dict)
                time.sleep(self.sleep_calculator(self._getTasks(filter=None)[0]))

    def loop(self):
        '''Starts the UI task thread and the regular task thread.'''
        # Starting separate threads ensures the UI thread never waits for the normal thread
        #   for example, it it gets rate limited
        UIThread = threading.Thread(target=self.UIloop)
        normalhread = threading.Thread(target=self.normalloop)
        UIThread.start()
        normalhread.start()
        UIThread.join()
        normalhread.join()

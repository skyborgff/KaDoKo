from typing import List
import random
import string
import time

# Todo: merge this task manaager and the tasker / Task manager

class Tasker():
    def __init__(self, taskDict: dict):
        self._taskDict = taskDict

    def addTask(self, task_name: str, args: List[str] = []):
        task, code = self._createTask(task_name, args)
        self._taskDict['tasks'] += [task]
        return code

    def getReply(self, code) -> str:
        test_reply = self._checkReply(code)
        while test_reply is None:
            test_reply = self._checkReply(code)
            time.sleep(0.1)
        return test_reply

    def addWaitReply(self, task_name: str, args: List[str] = []):
        code = self.addTask(task_name, args)
        return self.getReply(code)

    def _checkReply(self, code):
        '''Deletes the reply if it exists, and returns it'''
        real_reply = None
        for index in range(len(self._taskDict['replies'])):
            if self._taskDict['replies'][index]['code'] == code:
                real_reply = self._taskDict['replies'][index]['reply']
                self._taskDict['replies'].pop(index)
                continue
        return real_reply


    @staticmethod
    def _generateTaskCode():
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for _ in range(12))
        return result_str

    def _createTask(self, task_name: str, args: List[str]):
        task_code = self._generateTaskCode()
        task_dict = {'name': task_name,
                     'args': args,
                     'code': task_code,
                     'task_importance': 'UI',
                     'task_type': 'SYNC'}
        return task_dict, task_code

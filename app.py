import multiprocessing as mp
from multiprocessing import Process
import os
from Core.kadoko import Kadoko
import webbrowser
from Core.API.FlaskAPI import FlaskAPI
import time
from multiprocessing import Process, Manager
import logging
import os

if __name__ == '__main__':

    manager = Manager()
    d = manager.dict()

    d['tasks'] = manager.list()
    d['replies'] = manager.list()

    def run_flask(d):
        Flask = FlaskAPI(d)
        Flask.app.run(host='localhost', port='8283', debug=False)

    p2 = Process(target=Kadoko, args=(d,))
    p1 = Process(target=FlaskAPI, args=(d,))
    p1.start()
    p2.start()
    p1.join()

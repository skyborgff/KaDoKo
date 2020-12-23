import multiprocessing as mp
from multiprocessing import Process
import os
from Core.kadoki import Kadoki
import webbrowser
from Core.API.FlaskAPI import FlaskAPI
import time


kadoki = Kadoki()
kadoki.start()
FlaskAPI = FlaskAPI(kadoki)

FlaskAPI.app.run(host='localhost', port='8283', debug=False)


# def run_flask():
#     FlaskAPI.app.run(host='localhost', port='8283', debug=False)
#
# def start_kadoki():
#     kadoki.start()
#
#
#
# f = mp.Process(target=run_flask())
# k = mp.Process(target=start_kadoki())
#
# k.start()
# f.start()


# def on_websocket_close(page, sockets):
#     while not len(eel._websockets):
#         eel.sleep(0.5)  # We might have just refreshed. Give the websocket a moment to reconnect.
#
#
# eel.spawn(run_flask)
# eel.spawn(kadoki.start())
#
# eel.init('web')  # or the name of your directory
# eel.start('', mode=None, port=8282, disable_cache=True, close_callback=on_websocket_close, block=False)
#
# #webbrowser.open('http://localhost:8281/', new=2)
#
# # Maybe use gevent?
#
# while True:
#     print('awake')
#     eel.sleep(60)

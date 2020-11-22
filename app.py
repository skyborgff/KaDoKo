import eel
from Core.kadoki import Kadoki
import webbrowser
from Core.API.FlaskAPI import FlaskAPI

kadoki = Kadoki()
FlaskAPI = FlaskAPI(kadoki)

def run_flask():
    FlaskAPI.app.run(host='localhost', port='8283')

def on_websocket_close(page, sockets):
    while not len(eel._websockets):
        eel.sleep(0.5)  # We might have just refreshed. Give the websocket a moment to reconnect.


eel.spawn(run_flask)

eel.init('web')  # or the name of your directory
eel.start('', mode=None, port=8282, disable_cache=True, close_callback=on_websocket_close, block=False)

#webbrowser.open('http://localhost:8281/', new=2)

# Maybe use gevent?

while True:
    print('awake')
    eel.sleep(60)

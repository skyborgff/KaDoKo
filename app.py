import eel
from Core.kadoki import Kadoki
import webbrowser

kadoki = Kadoki()

@eel.expose
def first_launch():
    return kadoki.ui.first_launch()

@eel.expose
def library_list():
    return kadoki.ui.library_list()

@eel.expose
def db_list():
    return kadoki.ui.db_list()

@eel.expose
def set_start_settings(library, db):
    kadoki.settings.library = library
    kadoki.settings.db = db
    if not kadoki.plugins.all_authenticated():
        print(eel._js_functions)
        eel.route_to('Setup/Authenticate')


def on_websocket_close(page, sockets):
    while not len(eel._websockets):
        eel.sleep(0.5)  # We might have just refreshed. Give the websocket a moment to reconnect.

eel.init('web')  # or the name of your directory
eel.start('', mode='', port=8282, disable_cache=True, close_callback=on_websocket_close, block=False)
#webbrowser.open('http://localhost:8081/', new=2)


while True:
    print(eel._js_functions)
    eel.sleep(30)
    print('awake')
    #Main Loop
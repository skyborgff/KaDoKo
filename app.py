import eel
import time
from MAIN.master import Master

@eel.expose
def MALUserInfo():
    info = {}
    if mal.active:
        info = mal.user('@me')
        print(info)
    return info

@eel.expose
def MALAnimeInfo():
    info = {}
    if mal.active:
        info = mal.anime_list('@me')
        print(info)
    return info

@eel.expose
def MALConnected():
    return mal.active

@eel.expose
def MALConnect():
    return mal_url

@eel.expose
def MALRefresh():
    mal.refresh()
    return

@eel.expose
def MALANIDBConnect():
    master.connect_ids()
    return

@eel.expose
def MALAuthCode(code):
    if code == {}:
        return
    if not mal.active:
        mal.authenticate_code(code)
    return str(mal.active)

@eel.expose
def GetConnections():
    return master.get_connections()

master = Master()
mal = master.mal
mal_url = master.mal_auth()


def on_websocket_close(page, sockets):
    while not len(eel._websockets):
        eel.sleep(0.5)  # We might have just refreshed. Give the websocket a moment to reconnect.


eel.init('web')  # or the name of your directory
eel.start('index.html', mode='None', port=8282, disable_cache=True, close_callback=on_websocket_close, block=False)

while True:
    #Main Loop
    #Main Loop
    eel.sleep(5)
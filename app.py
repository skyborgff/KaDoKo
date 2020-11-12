import eel
import time
from MAIN.master import Master
import webbrowser

@eel.expose
def MALUserInfo():
    info = {}
    if mal.status==True:
        info = mal.user('@me')
        #print(info)
    return info

@eel.expose
def MALAnimeInfo():
    info = {}
    if mal.status==True:
        info = mal.anime_list('@me')
        #print(info)
    return info

@eel.expose
def MALConnected():
    return mal.status==True

@eel.expose
def ANIDBConnected():
    print(master.anidbudp.logged)
    return master.anidbudp.logged

@eel.expose
def ANIDBConnect(form):
    return master.anidbudp.auth(form["username"], form["password"])

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
    if not mal.status==True:
        mal.finish_auth(code)
    return str(mal.status==True)

@eel.expose
def GetConnections():
    return master.get_connections()

@eel.expose
def ConnectShows(mid, aid):
    master.connect_known(mid, aid)


master = Master()
mal = master.mal
mal_url = master.mal_auth()


def on_websocket_close(page, sockets):
    while not len(eel._websockets):
        eel.sleep(0.5)  # We might have just refreshed. Give the websocket a moment to reconnect.


def mal_ani():
    eel.sleep(5)
    mal.user('@me')
    mal.anime_list('@me')
    master.connect_ids('Total')
    #master.connect_ids('watching')
    eel.sleep(60 * 60 * 3)  # tri-Hourly grab


eel.spawn(mal_ani)

eel.init('web')  # or the name of your directory
eel.start('index.html', mode=None, port=8282, disable_cache=True, close_callback=on_websocket_close, block=False)
webbrowser.open('http://localhost:8081/', new=2)


while True:
    eel.sleep(60)
    print('awake')
    #Main Loop
    while not (mal.status == True):
        eel.sleep(10)

import json
import socket
import os

SERVER_ADDRESS_FILE = 'API/ANIDB/ANIDB_API_SERVER.json'
AUTH_INFO_FILE = "API/ANIDB/UDP_Auth.json"
LOCAL_PORT = 2048  # "If the API sees too many different UDP Ports from one IP within ~1 hour it will ban the IP"
INFO_client_name = "plexanidbsync"
INFO_client_version = "1"
INFO_api_version = "3"

class UDP_Client:
    def __init__(self, cache):
        self.logged = False
        self.clientname = INFO_client_name
        self.client_version = INFO_client_version
        self.api_version = INFO_api_version

        if os.path.exists(SERVER_ADDRESS_FILE):
            with open(SERVER_ADDRESS_FILE, 'r') as json_file:
                data = json.load(json_file)
                addrinfo = socket.getaddrinfo(data['ANIDB_HOSTNAME'], data['ANIDB_PORT'], proto=socket.IPPROTO_UDP)
                self.family = addrinfo[0][0]
                self.address = addrinfo[0][4]
                json_file.close()
        else:
            print('ERROR: ' + SERVER_ADDRESS_FILE + ' not found!')
            exit()
        self.open_socket()
        if os.path.exists(AUTH_INFO_FILE):
            with open(AUTH_INFO_FILE, 'r') as json_file:
                data = json.load(json_file)
                # remover após testes!
                self.username = data['ANIDB_USERNAME']
                self.password = data['ANIDB_PW']
                # remover após testes!
                json_file.close()
                self.logged = self.auth(self.username, self.password)

    def open_socket(self):
        self.socket = socket.socket(self.family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.bind(("0.0.0.0", LOCAL_PORT))

    def close_socket(self):
        self.socket.close()

    def communicate(self, message):
        self.socket.sendto(message.encode("ascii"), self.address)
        data = self.socket.recv(1024).decode("ascii")

    # print(data)

    def auth(self, username, password):
        print("Loggin in to ANIDB")
        auth_message = "AUTH user=" + username + "&pass=" + password + \
                       "&protover=" + self.api_version + "&client=" + self.clientname + "&clientver=" + \
                       self.client_version + "&nat=1"

        self.socket.sendto(auth_message.encode("ascii"), self.address)
        auth_response = self.socket.recv(1024).decode("ascii")
        print("AUTH response: " + auth_response)
        auth_response = auth_response.split()
        code = int(auth_response[0])
        print("code: " + str(code))
        if (code == 200 or code == 201):
            self.session_key = auth_response[1]
            if (int(auth_response[2].split(':')[1]) != LOCAL_PORT):  # ip:port
                print("WARNING: the client is behind a nat router!")
            # o router faz NAT e deve ser iniciada uma thread que faz PING periodicamente
            info = {"ANIDB_USERNAME": username, "ANIDB_PW": password}
            with open(AUTH_INFO_FILE, 'w') as outfile:
                json.dump(info, outfile)
            return True
        else:
            if code == 500:
                print("Prompt user for uname and pw")
                return False
            elif code == 502:
                print("ERROR! Exiting.")
                return False
            elif code == 503:
                print(
                    "Your client is outdated (protover too low) and no longer supported. Please update your client. Exiting.")
                return False
            elif code == 504:
                print("The client has been banned. Exiting.")
                return False
            elif code == 601:
                print("ANIDB out of service. Exiting.")
                return False
            else:
                print("ERROR " + str(code))
                return False

    def logout(self):
        self.socket.sendto(("LOGOUT s=" + self.session_key).encode("ascii"), self.address)
        logout_response = self.socket.recv(1024).decode("ascii")
        print("LOGOUT response: " + logout_response)

    def anime(self, title):
        anime_message = "ANIME aid=" + title + "&amask=ac20c000000000" + "&s=" + self.session_key
        # anime_message = "ANIME aname=" + title + "&s=" + self.session_key
        self.socket.sendto(anime_message.encode("ascii"), self.address)
        anime_response = self.socket.recv(1024).decode("ascii")
        print("ANIME response (" + title + "): " + anime_response)

    def byhash(self, size, ed2khash):
        byhash_message = "FILE size=" + size + "&ed2k=" + ed2khash + "&s=" + self.session_key
        self.socket.sendto(byhash_message.encode("ascii"), self.address)
        byhash_response = self.socket.recv(1024).decode("ascii")
        print("BYHASH response: " + byhash_response)

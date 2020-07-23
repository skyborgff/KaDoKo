import json
import socket
import os

SERVER_ADDRESS_FILE = 'ANIDB_API_SERVER.json'
class UDP_Client:
	def __init__(self):
		if os.path.exists(SERVER_ADDRESS_FILE):
			with open(SERVER_ADDRESS_FILE, 'r') as json_file:
				data = json.load(json_file)
				self.server_ip = socket.gethostbyname(data['ANIDB_HOSTNAME'])
				self.server_port = data['ANIDB_PORT']
		else:
			print('ERROR: ' + SERVER_ADDRESS_FILE + ' not found!')

	def connect_server(self):
		
import json
import socket
import os

SERVER_ADDRESS_FILE = 'API/ANIDB/ANIDB_API_SERVER.json'
class UDP_Client:
	def __init__(self):
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

	def open_socket(self):
		self.socket = socket.socket(self.family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

	def close_socket(self):
		self.socket.close()

	def communicate(self, message):
		self.socket.sendto(message.encode("ascii"), self.address)
		data = self.socket.recv(1024).decode("ascii")
		print(data)
import game

import socket
import sys

HOST = '192.168.25.7'
PORT = 5000

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print ('Falha ao criar socket')
	sys.exit()

try:
	remote_ip = socket.gethostbyname(HOST)
except socket.gaierror:
	print ('Hostname não encontrado. Encerrando...')
	sys.exit()

s.connect((remote_ip , PORT))
print ('Socket conectado ao host ' + HOST)

player_name = input("\nDigite seu nome: ")
try :
	s.sendall(str.encode(player_name))
except socket.error:
	print ('Falha ao enviar. Encerrando...')
	sys.exit()

data = s.recv(2048)
reply = data.decode('utf-8')
arr = reply.split(":")
print (arr[1])

g = game.Game(int(arr[0]),s)
g.run()

import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.25.5'
port = 5556

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Aguardando todos sobreviventes...")

currentId = "0"
pos = ["0:100,50", "1:200,100"] #player1, player2

def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            # recebe e decodifica client package
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Adeus!"))
                break
            else:
                #print("Recebido: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply #atualiza player pos

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                #print("Enviando: " + reply)
            # codifica e envia 
            conn.sendall(str.encode(reply))
        except:
            break

    print("Conexão de",currentId,"encerrada.") #
    conn.close()

while True:
    conn, addr = s.accept()
    print("Conectado", currentId, "em: ", addr)

    start_new_thread(threaded_client, (conn,))
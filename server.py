import socket
import select
import sys

class Player:
    def __init__(self, id):
        self.id = id
        self.name = ""
        self.pos = 0
        self.socket = ""
        
if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 2048
    SERVER = '192.168.25.7'
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(2)

    CONNECTION_LIST.append(server_socket)

    players = [Player(1), Player(2)]
    turn_now = -1
    game_status = -1
    running = False

    print('\nAguardando jogadores...\n')

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:

            # faz conexão com cliente
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print ("Jogador (%s, %s) conectado." % addr)

            else:   
                # processa os dados
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data: 
                        reply = data.decode('utf-8')
                        args = len(reply.split(","))             
                        # configura o game
                        if args == 1:
                            num_player = len(CONNECTION_LIST)-2
                            if num_player >= 2:
                                print ("ERROR: Quantidade de jogadores invalida. Encerrando...")
                                sys.exit()
                            else:
                                players[num_player].name = reply
                                print ("Jogador",players[num_player].name,"entrou no servidor.")
                                reply = (str(num_player)+':Bem-vindo(a) '+players[num_player].name+"!\n")
                                if len(CONNECTION_LIST)-1 == 2:
                                    running = True
                                else:
                                    running = False
                                sock.send(str.encode(reply))
                        elif args > 1:   
                            if not running:
                                sock.send(str.encode('0,1,conectando'))
                            else:   # game is running...
                                
                                this_id = int(reply.split(":")[0]) # id do player atual
                                other_id = swap_id(this_id) # id do adversario
                                print("Jogador atual:",players[this_id].name)
                                if this_id == turn_now: # se é a vez do player 
                                    print("Turno de:",players[this_id].name)
                                    arr = reply.split(":")[1].split(",")
                                    players[this_id].pos = arr[0] # posicao do player
                                    player_status = arr[1] # status do player
                                    
                                    # se player jogou, troca o turno
                                    if player_status == "jogou":
                                        turn_now = other_id
                                        msg = str(players[other_id].pos)+","+str(turn_now)+",aguardando"
                                    # se player nao jogou, mantém o turno
                                    else:
                                        msg = str(players[other_id].pos)+","+str(turn_now)+",jogando"
                                    sock.send(str.encode(msg))
                                else: 
                                    msg = str(players[other_id].pos)+","+str(turn_now)+",aguardando"
                                    sock.send(str.encode(msg))       
                except:
                    print ("ERROR: Jogador (%s,%s) desconectou-se." % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()

def swap_id(id):
    if id > 0:
        return 0
    return 1
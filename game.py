import pygame
import random
import sys

class Player():
    radius = 25 

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.color = color
        self.next_pos = -1

    def draw(self, g):
        pygame.draw.circle(g, self.color ,(self.x, self.y), self.radius,  0)

    def jump(self, b):
        if self.next_pos >= 26:
            return True
        pos_type = 0
        x, y, pos_type = b.get_position(self.next_pos)
        self.x, self.y = x,y
        if pos_type == 1:
            self.next_pos = self.next_pos + 1
            n = self.jump(b)
        elif pos_type == 2:
            self.next_pos = self.next_pos - 1
            n = self.jump(b)
        return False
            
class Game:
    turn = 0
    status = "conectando"

    def __init__(self, i, s, w = 800, h = 600):
        self.id = i
        self.socket = s
        self.width = w
        self.height = h
        self.player, self.player2 = self.setup_players()
        self.canvas = Canvas(self.width, self.height, "T1 - Marco Goedert")
        self.board = Board(self.canvas.get_canvas())
        self.info = Information(self.canvas)

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():

                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    run = False
                    pygame.quit()

                if self.status == "conectando":
                    self.canvas.draw_background()
                    self.board.draw()
                    self.info.play_button()
                    self.player.draw(self.canvas.get_canvas())
                    self.player2.draw(self.canvas.get_canvas())
                    self.info.awaiting_conn()
                else:
    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        width = self.canvas.width
                        height = self.canvas.height
                        if width-100 <= mouse[0] <= width and 0 <= mouse[1] <= 50: 
                            if self.id == self.turn:
                                # it's your turn
                                self.info.show_status("Jogador",self.id,"está jogando o dado...")
                                dice = random.randint(1,6)
                                print("Jogador",self.id,"rolou o dado e tirou",dice)
                                self.player.next_pos = self.player.next_pos + dice
                                self.ended = self.player.jump(self.board)
                                status = "jogou"
                                break
                            else:
                                # not your turn
                                print ("Aguarde o seu turno para jogar!")
                                self.info.awaiting_turn

            send = str(self.id)+":"+str(self.player.next_pos)+","+str(self.status)
            print("Jogador",str(self.id),"vai enviar:",send)
            self.player2.next_pos, self.turn, self.status = self.parse_data(self.send_data(send))
            
            #self.player.jump(self.board)
            #self.player2.jump(self.board)

            # Update Canvas
            self.canvas.draw_background()
            self.board.draw()
            self.info.play_button()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.info.awaiting_conn()
            self.info.show_turn(self.id, self.turn)

            """
            if (self.player2.connected == 0):
                self.info.awaiting_conn()
            elif (self.turn != self.id):
                self.info.awaiting_turn()
            if ended:
                self.info.show_status("Voce venceu! :D")
            """
            self.canvas.update()

        pygame.quit()

    def setup_players(self):
        orange = (242,207,1)
        black = (0,0,0)
        if self.id == 1:
            player1 = Player(50,25,orange)        
            player2 = Player(100,25,black)
        else:
            player1 = Player(50,25,black)        
            player2 = Player(100,25,orange)
        return player1, player2

    def send_data(self, msg):
        self.socket.sendall(str.encode(msg))
        try:
            data = self.socket.recv(2048)
            reply = data.decode('utf-8')
        except:
            print("ERROR: socket error")
            reply = "-1,-1,erro"
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(",")
            return int(d[0]), int(d[1]), d[2]
        except:
            return -1,-1,"erro"

class Information:
    def __init__(self, g):
        self.board = g
    
    def awaiting_conn(self):
        self.board.draw_text("Aguardando conexão...",32,800,600)

    def awaiting_turn(self):
        self.board.draw_text("Aguardando turno adversário...",32,800,600)

    def show_turn(self, player_id, turn):
        size = 16
        x = 800
        y = 50
        if turn == player_id:
            self.board.draw_text("Turno: Voce :)",size,x,y)
        else:
            self.board.draw_text("Turno: Adversario :(",size,x,y)
        
    def show_status(self, message):
        size = 16
        x = 800
        y = 90
        if message:
            self.board.draw_text(message,size,x,y)
        else:
            self.board.draw_text("Status: Sem status...",size,x,y)
    
    def play_button(self):
        x = self.board.width*2-100
        y = 40
        width = 100
        height = 40
        color_light = (170,170,170)

        self.board.draw_box(color_light,800,600,200,80)
        self.board.draw_text("Jogar",26,x,y)

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.display_surface = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.init()
        font = pygame.font.SysFont("Comic Sans MS", size)
        text = font.render(text, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (x // 2, y // 2) 
        self.display_surface.blit(text, text_rect)

    def draw_box(self, color, x, y, w, h):
        pygame.draw.rect(self.display_surface,color,(x,y,w,h),0)
        
    def get_canvas(self):
        return self.display_surface

    def draw_background(self):
        self.display_surface.fill((255,255,255))

class Board:

    def __init__(self, g):
        self.all_pos = []
        self.board = g
        self.create()
    
    def get_position(self, number):
        if number < 0 or number > len(self.all_pos):
            return 0,0,0
        else:
            x = self.all_pos[number].x
            y = self.all_pos[number].y
            t = self.all_pos[number].type
            return x,y,t

    def create(self):
        x = 50
        y = -10
        ptype = 2
        #top-down line
        for i in range(0,7): 
            y = y + 75
            if (len(self.all_pos) % 2) == 1:
                p = Position(x,y,ptype)
                if ptype > 1:
                    ptype = ptype - 1
                else:
                    ptype = ptype + 1
            else:
                p = Position(x,y)
            self.all_pos.append(p)

        #left-right line
        for i in range (0,4): 
            x = x + 75
            if (len(self.all_pos) % 2) == 1:
                p = Position(x,y,ptype)
                if ptype > 1:
                    ptype = ptype - 1
                else:
                    ptype = ptype + 1
            else:
                p = Position(x,y)
            self.all_pos.append(p)
        #down-top line
        for i in range (0,6): 
            y = y - 75
            if (len(self.all_pos) % 2) == 1:
                p = Position(x,y,ptype)
                if ptype > 1:
                    ptype = ptype - 1
                else:
                    ptype = ptype + 1
            else:
                p = Position(x,y)
            self.all_pos.append(p)
        #left-right line
        for i in range (0,4): 
            x = x + 75
            if (len(self.all_pos) % 2) == 1:
                p = Position(x,y,ptype)
                if ptype > 1:
                    ptype = ptype - 1
                else:
                    ptype = ptype + 1
            else:
                p = Position(x,y)
            self.all_pos.append(p)
        #top-down line
        for i in range(0,5): 
            y = y + 75
            if (len(self.all_pos) % 2) == 1:
                p = Position(x,y,ptype)
                if ptype > 1:
                    ptype = ptype - 1
                else:
                    ptype = ptype + 1
            else:
                p = Position(x,y)
            self.all_pos.append(p)

    def draw(self):
        for p in self.all_pos:
            p.draw(self.board)

class Position:
    width = height = 70

    def __init__(self, posx, posy, postype = 0):
        self.x = posx
        self.y = posy
        self.type = postype

    def draw(self, g):
        if self.type == 1:
            self.color =(14,224,5) #bom
        elif self.type == 2:
            self.color=(175,0,1) #ruim
        else:
            self.color=(191,191,191) #neutro
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
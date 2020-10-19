import pygame
from network import Network


class Player():
    width = height = 50 # to remove

    def __init__(self, startx, starty, color=(0,0,0)):
        self.x = startx
        self.y = starty 
        self.velocity = 2   # to remove
        self.color = color  # to remove

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)   # to remove

    def move(self, dirn):   # to update
        # as peças vao se mover porem em turnos
        # a peça deve se mover para o topo da casa
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity # to remove
        elif dirn == 1:
            self.x -= self.velocity # to remove
        elif dirn == 2:
            self.y -= self.velocity # to remove
        else:   
            self.y += self.velocity # to remove
        

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)        # os players estao nascendo bugados, rever condição
        self.player2 = Player(100,100)      # os players estao nascendo bugados, rever condição
        self.canvas = Canvas(self.width, self.height, "[T1 - Redes de Computadores] Marco Goedert") # add feature: nickname do player
        self.board = Board(self.canvas.get_canvas())

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:    # to remove
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:     # to remove
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:   # to remove
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]: # to remove
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.board.draw()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))

class Board():

    def __init__(self, g):
        self.all_pos = []
        self.board = g
        self.create()
    
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
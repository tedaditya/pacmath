#Initialization
import pygame,sys,random,math,time, asyncio
from pygame.locals import *
VERSION = "BETA v1.0" #current version
#Initialization & Default setup
HEIGHT = 900
WIDTH = 1200
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,100,255)
WHITE = (255,255,255)
BACKGROUND_COLOR = BLACK
SCREEN_SIZE = (WIDTH,HEIGHT)
FPS = 60

clock = pygame.time.Clock()

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Helper funtions
#Setup the display screen
def setup_graphics():
    pygame.mixer.init(22050,-16,2,4096)
    pygame.init()
    #pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('PacMath '+VERSION)
    return screen
 

#Load image
def load_image(name):
    return pygame.image.load(name).convert_alpha()

#Display a text
def draw_text(surface, text, coordinates,size,color):
    font = pygame.font.Font('ARCADE.TTF',size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, coordinates)

def draw_default(surface, text, coordinates,size,color):
    font = pygame.font.Font(None,size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, coordinates)
    
#Calculate the distance of two points to check collisions between objects
def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)



class Pillet:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.eaten = False
        self.image = load_image('pillet.png')

    def display(self):
        screen.blit(self.image,(self.x,self.y))


class Meat():
    def __init__(self,x,y,qa):
        self.x = x
        self.y = y
        self.question = qa[0]
        self.image = load_image('meat.png')
        
    def display(self):
        screen.blit(self.image,(self.x,self.y))
        
        

class Pacman:
    def __init__(self):
        self.x = HEIGHT/15*7
        self.y = HEIGHT/15*7
        self.image = load_image('pacmath_RIGHT.png')
        self.direction = 'RIGHT'

        
    def move(self,direction):
        if direction == 'UP':
            self.y -= 6
        if direction == 'DOWN':
            self.y += 6
        if direction == 'LEFT':
            self.x -= 6
        if direction =='RIGHT':
            self.x += 6
        self.direction = direction
        self.image = load_image('pacmath_'+self.direction+'.png')
        

    def display(self):
        screen.blit(self.image,(self.x,self.y))
    
class Ghost:
    def __init__(self,i,qa,x,y):
        self.order = i
        self.x = x
        self.y = y
        self.answer = qa[1]
        self.image = load_image('ghost_'+str(self.order)+'.png')
        self.direction = 'RIGHT'
        self.directions = ['RIGHT','LEFT','UP','DOWN']
        self.vulnerable = 0
        
    def move(self):
        if self.x % (HEIGHT/15) ==0 and self.y % (HEIGHT/15) == 0:
            self.coor = [int(self.x/(HEIGHT/15))+1,int(self.y/(HEIGHT/15))+1]
            self.direction = self.random_move(self.coor,main.board.board)
        if self.direction == 'UP':
            self.y -= 3
        if self.direction == 'DOWN':
            self.y += 3
        if self.direction == 'LEFT':
            self.x -= 3
        if self.direction =='RIGHT':
            self.x += 3
    
    def display(self):
        screen.blit(self.image,(self.x,self.y))
        draw_text(screen,self.answer,(self.x+10,self.y+20),30,BLACK)

    #A recursive function to let a ghost turn to a random direction when it's possible
    def random_move(self,coor,board):
        x = coor[0]
        y = coor[1]
        direction = random.choice(self.directions)
        
        if direction == 'RIGHT':
            if x < len(board)-1 and self.direction != 'LEFT':
                if board[x+1][y] == '*':
                    return 'RIGHT'
                else:
                    return self.random_move(coor,board)
            else:
                return self.random_move(coor,board)
            
        if direction == 'LEFT':
            if x > 0:
                if board[x-1][y] == '*' and self.direction != 'RIGHT':
                    return 'LEFT'
                else:
                    return self.random_move(coor,board)
            else:
                return self.random_move(coor,board)
            
        if direction == 'DOWN':
            if y < len(board)-1:
                if board[x][y+1] == '*' and self.direction != 'UP':
                    return 'DOWN'
                else:
                    return self.random_move(coor,board)
            else:
                return self.random_move(coor,board)
            
        if direction == 'UP':
            if y > 0:
                if board[x][y-1] == '*' and self.direction != 'DOWN':
                    return 'UP'
                else:
                    return self.random_move(coor,board)
            else:
                return self.random_move(coor,board)

class Board:
    def __init__(self,level):
        self.board = []
        
        #Read the board from the file corresponding to the current level
        fp = open('board'+str(level%5)+'.txt')
        for line in fp:
            l = []
            for i in line.strip():
                l.append(i)
            self.board.append(l)
        fp.close()

    def display(self):
        pygame.draw.rect(screen,BLUE,(0,0,HEIGHT,HEIGHT),2)
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j]=='_':
                    pygame.draw.rect(screen,BLUE,(HEIGHT/15*(i-1),HEIGHT/15*(j-1),HEIGHT/15,HEIGHT/15))

class Menu:
    def __init__(self):
        # Initialize menu
        self.pointer = 0
        self.imgs = []
        for i in range(3):
            self.imgs.append(load_image('MENU_' + str(i) + '.jpg'))
        pygame.mixer.Sound.play(menu)
        self.key = 0
    import time
    def update(self):
        keys_pressed = pygame.key.get_pressed() 

        if keys_pressed[pygame.K_UP] != 0 and self.pointer > 0:
            self.pointer -= 1
            time.sleep(0.1)  

        if keys_pressed[pygame.K_DOWN] != 0 and self.pointer < len(self.imgs) - 1:
            self.pointer += 1
            time.sleep(0.1)  

        if keys_pressed[pygame.K_RETURN]:
            if self.pointer == 0:
                main.mode = 'INITIALIZATION'
            elif self.pointer == 1:
                main.mode = 'LEADERBOARD'
            else:
                pygame.quit()
                sys.exit()

    def display(self):
        screen.blit(self.imgs[self.pointer], (0, 0))

class Leaderboard:
    def __init__(self):
        fp = open('leaderboard.txt')
        self.lb = []
        try:
            with open('leaderboard.txt', 'r') as fp:
                for line in fp:
                    data = line.strip().split(' ')
                    if len(data) == 2:  # Pastikan baris memiliki dua elemen
                        name = data[0]
                        try:
                            score = int(data[1])  # Coba mengonversi skor menjadi bilangan bulat
                            self.lb.append([name, score])
                        except ValueError:
                            print(f"Invalid score in line: {line.strip()}")
                    else:
                        print(f"Invalid line: {line.strip()}")
        except FileNotFoundError:
            print("File 'leaderboard.txt' not found.")

    def display(self):
        draw_text(screen,'HIGH SCORES',(400,50),72,WHITE)
        for i in range(min(10, len(self.lb))):  # Menyamakan panjang loop dengan panjang leaderboard
            if i < len(self.lb):
                draw_text(screen, self.lb[i][0],(280,200+50*i),48,WHITE)
                draw_text(screen, str(self.lb[i][1]),(780,200+50*i),48,WHITE)
        pass

        if (pygame.key.get_pressed()[pygame.K_ESCAPE] != 0 ):
            main.mode = 'MENU'

    def write(self, name, score):
        added = False
        for i in range(len(self.lb)):
            if self.lb[i][1] <= score:
                self.lb.insert(i, [name, score])
                added = True
                break
        if not added:  # Jika skor baru tidak dimasukkan di antara skor yang ada
            self.lb.append([name, score])

        try:
            with open('leaderboard.txt', 'w') as fp:
                for entry in self.lb:
                    fp.write(f"{entry[0]} {entry[1]}\n")
        except FileNotFoundError:
            print("File 'leaderboard.txt' not found.")
        
#The main game function where classes interact with each other
class Main:
    def __init__(self):
        self.level = 1
        #mode variable: 'MENU','INITIALIZATION','GAME','GAMEOVER','PAUSE','WIN','LEADERBOARD'
        self.mode = 'MENU'
        self.score = 0
        self.menu = Menu()
        self.leaderboard = Leaderboard()
        self.name = ''

        
    def display_menu(self):
        self.menu.update()
        self.menu.display()
        
        
        
    #Start a new level
    def start(self):
        self.pacman = Pacman()
        self.lives = 3

        #Questions and Answers
        self.qas = []
        while len(self.qas) < 4:
            qa = self.generate_question(self.level)
            if not self.qas:
                self.qas.append(qa)
            else:
                repeat = 0
                for i in self.qas:
                    if i[1] == qa[1]:
                        repeat = 1
                        break
                if not repeat:
                    self.qas.append(qa)
        
        self.ghosts = [Ghost(0,self.qas[0],0,0),Ghost(1,self.qas[1],HEIGHT*(14/15),0),Ghost(2,self.qas[2],0,HEIGHT*(14/15)),Ghost(3,self.qas[3],HEIGHT*(14/15),HEIGHT*(14/15))]
        self.board = Board(self.level)
        
        self.pillets = []
        for i in range(17):
            for j in range(17):
                if self.board.board[i][j] == '*':
                    self.pillets.append(Pillet(HEIGHT/15*(i-1),HEIGHT/15*(j-1)))
        self.meats = []
        while len(self.meats) < 4:
            pillet = random.choice(self.pillets)
            if pillet.x != HEIGHT/15*7 and pillet.y != HEIGHT/15*7:
                self.meats.append(Meat(pillet.x,pillet.y,self.qas[len(self.meats)]))
                self.pillets.remove(pillet)


        self.has_question = 0
        self.mode = 'GAME'

    #Generate a question for the level initiation
    def generate_question(self,level):
        if level%5 == 1:
            num1 = random.randint(4,6)
            num2 = random.randint(1,4)
            num3 = random.randint(1,3)
            result = num1+num2-num3
            if result >= 10:
                return [str(num1)+' + '+str(num2)+' - '+str(num3)+' = ',str(result)]
            if result < 10:
                return [str(num1)+' + '+str(num2)+' - '+str(num3)+' = ','0'+str(result)]

        elif level%5 == 2:
            num1 = random.randint(1,6)
            num2 = random.randint(1,6)
            num3 = random.randint(1,6)
            result = num1*num2+num3
            if result < 10 and result >= 0:
                return [str(num1)+' * '+str(num2)+' + '+str(num3)+' = ','0'+str(result)]
            else:
                return [str(num1)+' * '+str(num2)+' + '+str(num3)+' = ',str(result)]

        elif level%5 == 3:
            num1 = random.randint(1,5)
            num2 = random.randint(1,5)
            num3 = random.randint(1,5)
            num4 = random.randint(1,5)*num3
            result = num1*num2-int(num4/num3)
            if result < 10 and result >= 0:
                return [str(num1)+' * '+str(num2)+' - '+str(num4)+' / '+str(num3)+' = ','0'+str(result)]
            else:
                return [str(num1)+' * '+str(num2)+' - '+str(num4)+' / '+str(num3)+' = ',str(result)]

        elif level%5 == 4:
            num1 = random.randint(2,8)
            num2 = 2
            num3 = random.randint(1,5)
            num4 = random.randint(1,5)*num3
            result = num1*num2+int(num4/num3)
            if result < 10 and result >= 0:
                return [str(num1)+' * '+str(num2)+' + '+str(num4)+' / '+str(num3)+' = ','0'+str(result)]
            else:
                return [str(num1)+' * '+str(num2)+' + '+str(num4)+' / '+str(num3)+' = ',str(result)]
        
        elif level%5 == 0:
            num1 = random.randint(1,5)
            num2 = random.randint(1,5)
            num3 = 2
            num4 = random.randint(1,5)
            result = (num1+num2)/num3 + num4
            if result <10:
                return ['('+str(num1)+' + '+str(num2)+') / '+str(num3)+' + '+str(num4)+' = ','0'+str(result)]
            else:
                return ['('+str(num1)+' + '+str(num2)+') / '+str(num3)+' + '+str(num4)+' = ',str(result)]

    def move_pacman(self):
        
        #The coordinate of pacman on the board, including the current top-left positions, bottom-right positions and the corresponding positions after moving
        g = HEIGHT/15
        xa = int((self.pacman.x+10)/g)
        ya = int((self.pacman.y+10)/g)
        xb = int((self.pacman.x+52)/g)
        yb = int((self.pacman.y+50)/g)
        xc = int((self.pacman.x+4)/g)
        yc = int((self.pacman.y+4)/g)
        xd = int((self.pacman.x+58)/g)
        yd = int((self.pacman.y+56)/g)

        #Read user inputs
        if(pygame.key.get_pressed()[pygame.K_UP] != 0 ):
            if self.pacman.y > 0:
                if self.board.board[xa+1][yc+1] == '*' and self.board.board[xb+1][yc+1] == '*':
                    self.pacman.move('UP')
        elif(pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
            if self.pacman.y < HEIGHT - 50:
                if self.board.board[xa+1][yd+1] == '*' and self.board.board[xb+1][yd+1] == '*':
                    self.pacman.move('DOWN')
        elif(pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
            if self.pacman.x > 0:
                if self.board.board[xc+1][ya+1] == '*' and self.board.board[xc+1][yb+1] == '*':
                    self.pacman.move('LEFT')
        elif(pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
            if self.pacman.x < HEIGHT - 50:
                if self.board.board[xd+1][ya+1] == '*' and self.board.board[xd+1][yb+1] == '*':
                    self.pacman.move('RIGHT')

    #Check multiple in-game status
    def check(self):
        
        #Check collision between pacman and pillets
        for i in self.pillets:
            if dist(self.pacman.x,self.pacman.y,i.x,i.y) <= 20:
                self.pillets.remove(i)
                self.score += 100
                pygame.mixer.Sound.play(eatpillet)


        #Check collision between pacman and ghosts
        for i in self.ghosts:
            if dist(self.pacman.x,self.pacman.y,i.x,i.y) <= 20:
                if i.vulnerable == 0:
                    self.lives -= 1
                    self.pacman = Pacman()
                    pygame.mixer.Sound.play(death)

                if i.vulnerable == 1:
                    self.ghosts.remove(i)
                    self.score += 1000
                    self.has_question = 0
                    pygame.mixer.Sound.play(eatghost)


        
        #Check meats
        if self.has_question == 0:
            self.question = 'Please eat a meat.'
            for i in self.meats:
                if dist(self.pacman.x,self.pacman.y,i.x,i.y) <= 20:
                    self.has_question = 1
                    self.ghosts[self.meats.index(i)].vulnerable = 1
                    self.question = i.question
                    self.meats.remove(i)
                    pygame.mixer.Sound.play(eatmeat)

                                
        
        #Check gameover
        if self.lives == 0:
            self.mode = 'GAMEOVER'

            
        #Check win
        if not self.ghosts:
            self.mode = 'WIN'

        #Check pause
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] != 0 ):
            self.mode = 'PAUSE'

    def gameover(self):
        finish = 0
        while not finish:
            screen.fill(BLACK)
            draw_text(screen,'GAMEOVER',(330,50),128,BLUE)
            draw_text(screen,'Your score is '+str(self.score),(350,300),48,WHITE)
            draw_text(screen,'Please enter your name',(350,370),48,WHITE)
            pygame.draw.rect(screen,WHITE,(350,440,500,50),5)
            draw_text(screen,self.name,(360,440),50,WHITE)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        self.name += event.unicode
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key ==K_RETURN:
                        self.leaderboard.write(self.name,self.score)
                        self.score = 0
                        self.level = 1
                        self.menu = Menu()
                        self.mode = 'MENU'
                        finish = 1
            pygame.display.flip()
        
    #The main game loop       
    async def game(self):
        while True:
            #Setting maxmimum FPS
            clock.tick(FPS)

            #Setting QUIT event
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #Fill the screen with black
            screen.fill(BLACK)

            if self.mode == 'MENU':
                self.display_menu()
                if self.menu.key:
                    time.sleep(0.01)

            #Initialize a level                   
            if self.mode == 'INITIALIZATION':
                self.start()

            #In-game loops
            if self.mode == 'GAME':
                #Update
                self.move_pacman()
                for i in self.ghosts:
                    i.move()


                #Check
                self.check()

                
                #Draw objects
                for i in self.pillets:
                    i.display()
                for i in self.meats:
                    i.display()
                self.board.display()
                self.pacman.display()
                for i in self.ghosts:
                    i.display()

                #Draw texts
                draw_text(screen,'Level: '+str(self.level),(HEIGHT+10,0),24,WHITE)
                draw_text(screen,'Lives: '+str(self.lives),(HEIGHT+10,20),24,WHITE)
                draw_text(screen,'Score: '+str(self.score),(HEIGHT+10,50),24,WHITE)
                draw_text(screen,'1. Gunakan Tombol Panah',(HEIGHT+10,80),24,WHITE)
                draw_text(screen,'untuk Mengontrol PacMath.',(HEIGHT+10,110),24,WHITE)
                draw_text(screen,'2. Hilangkan semua hantu ',(HEIGHT+10,140),24,WHITE)
                draw_text(screen,'dengan cara menjawab soal',(HEIGHT+10,170),24,WHITE)
                draw_text(screen,'didalam buah.',(HEIGHT+10,200),24,WHITE)
                draw_text(screen,'3. Hilangkan Semua Pillet',(HEIGHT+10,230),24,WHITE)
                draw_text(screen,'untuk Mendapatkan Score ',(HEIGHT+10,260),24,WHITE)
                draw_text(screen,'Tertinggi.',(HEIGHT+10,290),24,WHITE)
                draw_default(screen,self.question,(HEIGHT+10,320),30,RED)
                
            #Gameover
            #Currently under development, restarts level 1 automatically
            if self.mode == 'GAMEOVER':
                self.gameover()

                


            #Winning
            #Currently under development, restarts level 1 automatically
            if self.mode == 'WIN':
                self.level += 1
                self.mode = 'INITIALIZATION'

            if self.mode == 'PAUSE':
                draw_text(screen,'PAUSED',(560,440),36,WHITE)
                draw_text(screen,'PRESS ENTER TO CONTINUE',(400,480),36,WHITE)
                if (pygame.key.get_pressed()[pygame.K_RETURN] != 0 ):
                    self.mode = 'GAME'

            if self.mode == 'LEADERBOARD':
                self.leaderboard.display()
            #Flip
            pygame.display.flip()
            await asyncio.sleep(0)



screen = setup_graphics()
menu = pygame.mixer.Sound('menu.ogg')
death = pygame.mixer.Sound('death.ogg')
eatpillet = pygame.mixer.Sound('eatpillet.ogg')
eatghost = pygame.mixer.Sound('eatghost.ogg')
eatmeat = pygame.mixer.Sound('eatmeat.ogg')
main = Main()

asyncio.run(main.game())

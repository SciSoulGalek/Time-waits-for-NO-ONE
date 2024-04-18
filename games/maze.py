import os
import sys
import random
import pygame

WHITE = (255,255,255) 
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(20, 20, 20, 20)
        self.image = pygame.image.load("sprites/maze/player.png")
        self.counter = 3
 
    def move(self, dx, dy):
        speed = 1
        if dx != 0:
            self.move_single_axis(dx * speed, 0)
        if dy != 0:
            self.move_single_axis(0, dy * speed)
    
    def move_single_axis(self, dx, dy):
   
        self.rect.x += dx
        self.rect.y += dy
 
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
        for door in doors:
            if self.rect.colliderect(door.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = door.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = door.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = door.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = door.rect.bottom

        for key in keys:
            if self.rect.colliderect(key.rect):
                key.rect.x = 2000
                key.rect.y = 2000
                self.counter -= 1
 

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        super().__init__()
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
        self.image = pygame.image.load("sprites/maze/wall.png")
        
class Key(pygame.sprite.Sprite):
     
     def __init__(self,pos):
         super().__init__()
         keys.append(self)
         self.rect = pygame.Rect(pos[0], pos[1],20,20)
         self.image = pygame.image.load("sprites/maze/key.png")

class Door(pygame.sprite.Sprite):
     
     def __init__(self,pos):
         super().__init__()
         doors.append(self)
         self.rect = pygame.Rect(pos[0], pos[1],20,20)
         self.image = pygame.image.load("sprites/maze/door.png")   

class Escape(pygame.sprite.Sprite):

     def __init__(self,pos):
         super().__init__()
         escapes.append(self)
         self.rect = pygame.Rect(pos[0],pos[1],20,20)  
         self.image = pygame.image.load("sprites/maze/exit.png")      


pygame.init()
font = pygame.font.SysFont("Times New Roman" , 40)
all_sprites_list = pygame.sprite.Group()
 
pygame.display.set_caption("Maze game")
screen = pygame.display.set_mode((800, 800))
 
clock = pygame.time.Clock()
escapes = []
doors = []
keys = []
walls = [] 
player = Player() 


all_sprites_list.add(player)


level =  [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W   W        W     W        W      W   W",
"W W W WW WWWWWWWW WWWW WWWW WWWWW  W   W",
"W W             W       W     W      WWW",
"W     WWWWWWW WWWWWWWW  W WWWWWWWWWW   W",
"WWW    W     W        W     W          W",
"W WWWW W WWW W WWWWW WWWW  WW WWWW W W W",
"W W        W             W  W  W     W W",
"W WWWWWWWW WWWWW WWWW WWWW  W   WWW    W",
"W        W      W     W     W   W    W W",
"WWWWW WWWW  WWWWWW WWWW  WWWWWW  WWW W W",
"W      W        W   W           W W    W",
"W WW WWWWWW WWW WWWW  WWWWW W   WW  WWWW",
"W W    W      W    W      W    WW  WW  W",
"W WW WWWW WWWWWW WWWWW  WWWW WWWW WW   W",
"W W     W     W      W        W     WW W",
"W W  WW WWWWW WWWW W WWW WWWWWWWW W    W",
"W W   W    W         W        W     W WW",
"W WWWWW WWWW WWWWWWW  W W WWWWW WWW W  W",
"W     W    W   W        W    W   W   W W",
"W WWWWWWWWWW WWWW WWWWWWWWWW WWW W W  WW",
"W W      W    W         W       W   W  W",
"W W  WWWWWWWWWWWWWW  W WWWWWWWWWW  W  WW",
"W W        W        W     W        W  WW",
"W WW WWWWW  W  WWWWWWW WWWWWWW WWWW  WWW",
"W     W         W         W    W     DEW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]
 
# Parse the level string above. W = wall, E = exit
reps = 3
flag1 = True
flag2 = True
flag3 = True
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            escape = Escape((x,y))
            pygame.draw.rect(screen,(255,255,255),escape.rect)
            all_sprites_list.add(escape)
        if col == "D":
            Door((x,y))
        if col == " " and reps != 0:
            if x > 280 and y < 260 and flag1:  #random spawn of keys
                if(random.random() < 0.1):
                    Key((x,y))
                    flag1 = False
                    reps -= 1
            if x < 150 and y > 260 and flag2:
                if(random.random() < 0.1):
                    Key((x,y))
                    flag2 = False
                    reps -= 1
            if x > 500 and y > 260 and flag3:
                if(random.random() < 0.1):
                    Key((x,y))
                    flag3 = False
                    reps -= 1




        x += 20
    y += 20
    x = 0

text1 = font.render('Door Opened! Find Exit!',True,WHITE)
option = font.render('Play(press 1)',True,WHITE)
option2 = font.render('Quit(press 2)',True,WHITE)
header = font.render('Escape from Dungeon',True,WHITE)
running = True
playing = False
while running:
    screen.fill((0,0,0))
    screen.blit(header,(240,200))
    screen.blit(option,(300,300))
    screen.blit(option2,(300,400))
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    key = pygame.key.get_pressed()
    if key[pygame.K_1]:
        playing = True
    if key[pygame.K_2]:
        running = False
        sys.exit()

    

    while playing:
    
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                playing = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                playing = False
 
   
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)
        
 
    
 
    
        if player.rect.colliderect(escape.rect):
            playing = False
        
    
    
        screen.fill((0, 0, 0))
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 0), wall.rect)
            all_sprites_list.add(wall)
        for key in keys:
            pygame.draw.rect(screen,(0,0,0), key.rect)
            all_sprites_list.add(key)
        for door in doors:
            pygame.draw.rect(screen,(0,0,0), door.rect)
            all_sprites_list.add(door)
    
        if player.counter == 0:
            door.rect.x = 2000
            door.rect.y = 2000
            screen.blit(text1,(200,700))
    
        
        pygame.draw.rect(screen, (0, 0, 0), player.rect)
        all_sprites_list.draw(screen)
        pygame.draw.circle(screen, BLACK,(player.rect.x + 8 , player.rect.y + 8), 1000, 950) #for limited vision, delete this line of code to remove limited vision
        text = font.render('Keys left: '+ str(player.counter) + "(find 3 keys to unlock the door)" , True, WHITE, BLACK)
        screen.blit(text,(70,650))
        pygame.display.update()
        clock.tick(100)

    pygame.display.update()


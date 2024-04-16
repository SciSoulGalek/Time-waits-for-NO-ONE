import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SPEED = 5
SCORE = 0
coinscore = 0
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, "black")
background = pygame.image.load("Lab10/images/AnimatedStreet.png")
coin = pygame.image.load("Lab10/images/coin.png")
coini = 0
coins = 0

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Lab10/images/blue.png")
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Lab10/images/red.png")
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(32, SCREEN_WIDTH - 32), -31)
        self.weight = random.randint(1, 3)  # Assign random weight to the coin

    def move(self):
        global coinscore
        self.rect.move_ip(0, 10)
        if self.rect.top > 600:
            self.rect.top = -62
            self.rect.center = (random.randint(32, SCREEN_WIDTH - 32), -31)
        elif self.rect.colliderect(P1):
            # Random weight to the coinscore
            coinscore += self.weight  
            self.rect.top = -62
            self.rect.center = (random.randint(32, SCREEN_WIDTH - 32), -31)


# Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

#  Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
Coins = pygame.sprite.Group()
Coins.add(C1)

#  a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
bgy = 0
coin_y = -62
coin_x = 0
y = 0
bgsound = pygame.mixer.Sound("Lab10/sound/background.wav")
bgsound.play()

# Game Loop
while True:
    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, bgy))
    DISPLAYSURF.blit(background, (0, bgy - 600))

    if bgy < 600:
        bgy += 7
    else:
        bgy = 0

    scores = font_small.render(str(SCORE), True, "BLACK")
    coinscores = font_small.render(str(coinscore), True, "BLACK")
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coinscores, (360, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    for el in Coins:
        DISPLAYSURF.blit(el.image, el.rect)
        el.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        bgsound.stop()
        pygame.mixer.Sound('Lab10/music/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill("RED")
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    # after N coins increase the enemy speed
    if coinscore >= 3:  
        SPEED += 0.05  # Increase enemy speed
        

    pygame.display.update()
    FramePerSec.tick(FPS)
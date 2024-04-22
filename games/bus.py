import pygame
from pygame.locals import *
SCORE = 0

def play():
    #Imports
    import random, time, sys
    from datetime import datetime
    
    #Initializing 
    pygame.init()
    pygame.mixer.init()
    
    #Setting up FPS 
    FPS = 60
    FramePerSec = pygame.time.Clock()
    
    #Creating colors
    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    #Other Variables for use in the program
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 700
    SPEED = 3
    COINS = 0
    FUEL = 100
    
    #Setting up Fonts
    font = pygame.font.SysFont("Verdana", 60)
    font_normal = pygame.font.SysFont("Verdana", 40)
    font_small = pygame.font.SysFont("Verdana", 20)
    game_over = font.render("Game Over", True, BLACK)
    
    #music
    pygame.mixer.music.load('sound/bus/background.wav')
    pygame.mixer.music.play(-1)
    
    #Background 
    background = pygame.image.load("sprites/bus/racerbg.png")
    background = pygame.transform.scale(background, (1100, 700))
    # background = pygame.transform.rotate(background, 90)
    background_x = 0 
    
    #Create a white screen 
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game")


    #Enemy class
    class Enemy(pygame.sprite.Sprite):
          def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("sprites/bus/Enemy.png")
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT - 40))  
    
          def move(self):
            global SCORE
            self.rect.move_ip(-(SPEED + 2 + COINS / 100), 0)
            if (self.rect.left < 0):
                SCORE += 1
                self.rect.left = SCREEN_WIDTH + 100
                self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT - 40))
    
    #Player class 
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("sprites/bus/bus.png")
            self.rect = self.image.get_rect()
            self.rect.center = (160, 520)
            
        def move(self):
            pressed_keys = pygame.key.get_pressed()
            if self.rect.top > 100:
                if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -5)
            if self.rect.bottom < SCREEN_HEIGHT - 100: 
                if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0,5)
             
            if self.rect.left > 0:
                  if pressed_keys[K_LEFT]:
                      self.rect.move_ip(-5, 0)
            if self.rect.right < SCREEN_WIDTH:        
                  if pressed_keys[K_RIGHT]:
                      self.rect.move_ip(5, 0)
    
    #Coin class
    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("sprites/bus/coin.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH + (SPEED * 100), random.randint(40, SCREEN_HEIGHT - 40)) 
    
        def move(self):
            self.rect.move_ip(-SPEED, 0)
            if (self.rect.left < 0):
                self.rect.left = SCREEN_WIDTH + 50
                self.rect.center = (SCREEN_WIDTH + (SPEED * 100), random.randint(40, SCREEN_HEIGHT - 40))
    
    #Better coin class
    class Better_Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("sprites/bus/coin.png")
            self.image = pygame.transform.scale(self.image, (25, 25))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH + (SPEED * 500), random.randint(40, SCREEN_HEIGHT - 40)) 
    
        def move(self):
            self.rect.move_ip(-SPEED, 0)
            if (self.rect.left < 0):
                self.rect.center = (SCREEN_WIDTH + (SPEED * 500), random.randint(40, SCREEN_HEIGHT - 40))
    
    #Fuel class
    class Fuel(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("sprites/bus/fuel.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH + (SPEED * 100), random.randint(40, SCREEN_HEIGHT - 40)) 
    
        def move(self):
            self.rect.move_ip(-SPEED, 0)
            if (self.rect.left < 0):
                self.rect.center = (SCREEN_WIDTH + (SPEED * 100), random.randint(40, SCREEN_HEIGHT - 40))
    
    #Setting up Sprites        
    P1 = Player()
    E1 = Enemy()
    C = Coin()
    B = Better_Coin()
    F = Fuel()
    
    #Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coin = pygame.sprite.Group()
    coin.add(C)
    better_coin = pygame.sprite.Group()
    better_coin.add(B)
    fuel = pygame.sprite.Group()
    fuel.add(F)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C)
    all_sprites.add(B)
    all_sprites.add(F)
    
    # Fuel bar variables
    FUEL = 100
    fuel_bar_width = 100
    fuel_bar_height = 10
    fuel_bar_pos = (10, SCREEN_HEIGHT - 30)
    fuel_decrease_rate = 0.1  # Rate at which fuel decreases per frame
    
    #Get the highscore to display
    f = open('highscore.txt', 'r')
    HS = f.readline()
    HS = int(HS)
    
    #Start time
    start_time = datetime.now()

    #Adding a new User event(speed increases every second) 
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    #Game Loop
    while True: 
        for event in pygame.event.get():
            #Increase speed
            if event.type == INC_SPEED:
                if SPEED < 10: 
                    SPEED += 0.05     
            #Quit
            if event.type == QUIT:
                pygame.mixer.music.stop()
                return
            
        # Calculate elapsed time
        elapsed_time = datetime.now() - start_time
        # Convert elapsed time to a string
        timer_text = str(elapsed_time)
        # Extract minutes and seconds
        minutes = elapsed_time.seconds // 60
        seconds = elapsed_time.seconds % 60
        # Format minutes and seconds into a string
        timer_text = "{:02}:{:02}".format(minutes, seconds)


        #Move the background to create animation effect
        background_x -= SPEED - 0.4
        if -background_x >= SCREEN_WIDTH:
            background_x = 0

        #Display the background
        DISPLAYSURF.blit(background, (background_x, 0))
        DISPLAYSURF.blit(background, (background_x + SCREEN_WIDTH, 0))

        #Draw fuel bar
        pygame.draw.rect(DISPLAYSURF, GREEN, (fuel_bar_pos[0], fuel_bar_pos[1], FUEL, fuel_bar_height))
        pygame.draw.rect(DISPLAYSURF, BLACK, (fuel_bar_pos[0], fuel_bar_pos[1], fuel_bar_width, fuel_bar_height), 2)

        #Decrease fuel over time
        FUEL -= fuel_decrease_rate

        #Display score, highscore and coins
        highscore = font_small.render(f'Highscore:{HS}', True, BLACK)
        scores = font_small.render(str(SCORE), True, BLACK)
        if HS <= SCORE:
            HS = SCORE
        DISPLAYSURF.blit(highscore, (10,10))
        DISPLAYSURF.blit(scores, (10,30))
        coins = font_small.render(str(COINS), True, BLACK)
        DISPLAYSURF.blit(coins, (360,10))

        # Render text
        text_surface = font_normal.render(timer_text, True, (255, 255, 255))
        DISPLAYSURF.blit(text_surface, (1100 - text_surface.get_width(), 0))

        if SPEED < 10:
            speed = font_small.render(f'Speed:{str(round(SPEED, 2))}', True, BLACK)
            DISPLAYSURF.blit(speed, (SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT - 50))
        else:
            speed = font_small.render(f'Speed:10(MAX)', True, BLACK)
            DISPLAYSURF.blit(speed, (SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT - 50))

        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        #Collecting coin
        if pygame.sprite.spritecollideany(P1, coin):
            pygame.mixer.Sound('sound/bus/catch.mp3').play()
            COINS += 1
            collided_coin = pygame.sprite.spritecollideany(P1, coin)
            collided_coin.rect.center = (-(SPEED * 100), random.randint(40, SCREEN_WIDTH - 40))

        #Collecting better coin
        if pygame.sprite.spritecollideany(P1, better_coin):
            pygame.mixer.Sound('sound/bus/catch.mp3').play()
            COINS += 3
            collided_better_coin = pygame.sprite.spritecollideany(P1, better_coin)
            collided_better_coin.rect.center = (-(SPEED * 500), random.randint(40, SCREEN_WIDTH - 40))

        #Collecting fuel
        if pygame.sprite.spritecollideany(P1, fuel):
            pygame.mixer.Sound('sound/bus/catch.mp3').play()
            FUEL = min(100, FUEL + 20)
            collided_fuel = pygame.sprite.spritecollideany(P1, fuel)
            collided_fuel.rect.center = (-(SPEED * 100), random.randint(40, SCREEN_WIDTH - 40))

        #Game over part
        if pygame.sprite.spritecollideany(P1, enemies) or FUEL < 0:
            pygame.mixer.music.stop()
            pygame.mixer.Sound('sound/bus/crash.wav').play()
            time.sleep(1)
            #Save the highscore
            f = open('highscore.txt', 'w')
            f.write(str(HS))   

            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))

            pygame.display.update()
            for entity in all_sprites:
                entity.kill() 
            time.sleep(2)
            return        
        pygame.display.update()
        FramePerSec.tick(FPS)
def play(text):
    import os
    import sys
    import random
    import pygame
    from datetime import datetime
    pygame.init()

    # colors
    WHITE = (255,255,255) 
    BLACK = (0, 0, 0)

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(20, 20, 20, 20)
            self.image = pygame.image.load("sprites/maze/player.png")
            self.image = pygame.transform.scale(self.image, (16, 20))
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

    class Escape(pygame.sprite.Sprite):

         def __init__(self,pos):
             super().__init__()
             escapes.append(self)
             self.rect = pygame.Rect(pos[0], pos[1], 20, 20)  
             self.image = pygame.image.load("sprites/maze/exit.png")      


    font = pygame.font.SysFont('Aries', 40)
    all_sprites_list = pygame.sprite.Group()
    
    pygame.display.set_caption("Find the way to KBTU")
    screen = pygame.display.set_mode((1100, 700))
    
    clock = pygame.time.Clock()
    escapes = []
    keys = []
    walls = [] 
    player = Player() 


    all_sprites_list.add(player)


    level =  [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW     ",
    "W   W        W     W        W      W             W     ",
    "W W W WW WWWWWWWW WWWW WWWW WWWWW  W  WWWWWWWWWW W     ",
    "W W             W       W             W          WWWWWW",
    "W     WWWWWWW WWWWWWWW  W WWWWWWWWWWWWW WWW WWWW      W",
    "WWW    W     W        W     W           W    W WWWWWW W",
    "W WWWW W WWW W WWWWW WWWW  WW WWWW W WWWW  WWW W      W",
    "W W        W             W  W  W     W       W WWWW WWW",
    "W WWWWWWWW WWWWW WWWW WWWW  W   WWWW   WWWWW W W  W W W",
    "W        W      W     W     W   W    W   W     WW   W W",
    "WWWWW WWWW  WWWWWW WWWW  WWWWWW  WWW WW  WWWWW  W WWW W",
    "W      W        W   W           WWW   W      WW W W   W",
    "W WW WWWWWWWWWW WWWWW WWWWW W   W   W WWWW W  W W   WWW",
    "W W    W      W    WW     W     W W W W    WW W WW    W",
    "W WW WWWW WWWWWW WWWWW  WWWW WWWW WW   W W  W W   W  WW",
    "W W           W      W        W     WW   WW W W W  W  W",
    "W W  WW WWWWW WWWW W WWW WWWWWWWW W   WW  W W   WW W  W",
    "W W   W    W         W        W     W  WWWW WWWW      W",
    "W WWWWW WWWW WWWWWWW WWWW WWWWWWWWW WW         W WWWW W",
    "W     W    W   W        W    W   W   WWWWWWWWW W W    W",
    "W WWWWWWWWWW WWWW WWWWWWWWWW WWW WWW  W      W WWW WWWW",
    "W W      W    W         W           W WW  WW   W      W",
    "W W  WWWWWWWWWWWWWW  W WWWWWWWWWW  W   WW  WWWWW WWWW W",
    "W W          W       W     W        W   WW     W      W",
    "W WW WWWWWWW W WWWWWWW WWWWWW WWWWWWWWW WWWWW WWWW W WW",
    "W W   W    W   W    W  W  W   W         W   W W    W  W",
    "W     W WW WWWWW WW W WW  W W W WWW WWW W W W W WW WW W",
    "W WWWWW W         W W     W W W   WWW   W W   W  W W  W",
    "W   W   WWWWWWWWWWW WWWWW W W W W     W W WWWWWW W W WW",
    "W W W WWW         W       W W W WWWW WWWW        W    W",
    "W W W   WW W  W W WWWWWWWWW W W    W    W WWWW W WWWW W",
    "W W W W    WWWW W       W W W WWWW WWW WW      W      W",
    "W WWW W WWWW    WWW WWWWW   W    W   W  WWWW WWWWW WWWW",
    "W     W      W  W         W W WW   W    W            EW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]
    
    # Parse the level string above. W = wall, E = exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                escape = Escape((x,y))
                pygame.draw.rect(screen,(255,255,255),escape.rect)
                all_sprites_list.add(escape)
            x += 20
        y += 20
        x = 0

    #Start time
    start_time = datetime.now()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        # Calculate elapsed time
        elapsed_time = datetime.now() - start_time
        # Convert elapsed time to a string
        timer_text = str(elapsed_time)
        # Extract minutes and seconds
        minutes = elapsed_time.seconds // 60
        seconds = elapsed_time.seconds % 60
        # Format minutes and seconds into a string
        timer_text = "{:02}:{:02}".format(minutes, seconds)


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
            running = False
        screen.fill('Gray')
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 0), wall.rect)
            all_sprites_list.add(wall)
        for key in keys:
            pygame.draw.rect(screen,(0,0,0), key.rect)
            all_sprites_list.add(key)

        pygame.draw.rect(screen, (0, 0, 0), player.rect)
        all_sprites_list.draw(screen)
        
        # Render text
        text_surface = font.render(timer_text, True, (255, 255, 255))
        screen.blit(text_surface, (1050 - text_surface.get_width() // 2, 20))
        
        pygame.display.update()
        clock.tick(100)

        pygame.display.update()

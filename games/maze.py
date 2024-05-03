def play():
    import os
    import sys
    import random
    import pygame
    from datetime import datetime, timedelta
    pygame.init()

    # colors
    WHITE = (255,255,255) 
    BLACK = (0, 0, 0)
    DARK_GRAY = (108, 108, 108)

    wall_choose = ['roof1', 'roof2', 'roof3', 'roof4', 'roof5', 'tree1', 'tree2', 'flower']
    
    lose_screen1 = pygame.image.load("sprites/final/lose.png")
    lose_screen2 = pygame.image.load("sprites/final/losech.png")
    lose_screen3 = pygame.image.load("sprites/main/yourelateloss.png")

    global direction
    direction = 'right'
    
    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(20, 20, 20, 20)
            self.image = pygame.image.load("sprites/maze/player.png") 
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.direction = 'right'
            self.counter = 3
            self.add_time = False  # Variable to track whether to add or subtract time
            self.sub_time = False  # Variable to track whether to add or subtract time

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
                    if key.key_type == 'greenapple':
                        self.add_time = True  # Set add_time to True when picking up a green apple
                    elif key.key_type == 'redapple':
                        self.sub_time = True  # Set add_time to False when picking up a red apple
                    key.rect.x = 2000
                    key.rect.y = 2000
                    self.counter -= 1

                    
        def draw(self, surface):
            if self.direction == 'left':
                rotated_image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                rotated_image = pygame.transform.rotate(self.image, -90)
            elif self.direction == 'down':
                rotated_image = pygame.transform.rotate(self.image, 180)
            else:
                rotated_image = self.image

            surface.blit(rotated_image, self.rect)

    class Wall(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
            self.image = pygame.image.load(f"sprites/maze/{wall_choose[random.randint(0, 7)]}.png")

    class Key(pygame.sprite.Sprite):

        def __init__(self, pos, key_type):
            super().__init__()
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
            if key_type == 'greenapple':
                self.image = pygame.image.load("sprites/maze/greenapple.png")
            elif key_type == 'redapple':
                self.image = pygame.image.load("sprites/maze/redapple.png")
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.key_type = key_type

    class Escape(pygame.sprite.Sprite):

         def __init__(self, pos):
             super().__init__()
             escapes.append(self)
             self.rect = pygame.Rect(pos[0], pos[1], 20, 20)  
             self.image = pygame.image.load("sprites/maze/exit.png")      


    font = pygame.font.Font("fonts/superfont.ttf", 23)
    all_sprites_list = pygame.sprite.Group()
    
    pygame.display.set_caption("Find the way to KBTU")
    screen = pygame.display.set_mode((1100, 700))
    
    clock = pygame.time.Clock()
    escapes = []
    keys = []
    walls = [] 
    player = Player() 

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

    # Determine the number of keys of each type
    num_gold_keys = 3
    num_silver_keys = 3

    # Keep track of available positions to place keys
    available_positions = []

    # Iterate through the level to find available positions
    for y, row in enumerate(level):
        for x, col in enumerate(row):
            if col == ' ':
                available_positions.append((x * 20, y * 20))  # Convert grid position to pixel position

    # Shuffle the available positions
    random.shuffle(available_positions)

    # Create gold keys
    for _ in range(num_gold_keys):
        if available_positions:
            pos = available_positions.pop()
            keys.append(Key(pos, 'greenapple'))

    # Create silver keys
    for _ in range(num_silver_keys):
        if available_positions:
            pos = available_positions.pop()
            keys.append(Key(pos, 'redapple'))


    #Start time
    start_time = datetime.strptime("08:30", "%H:%M")
    add_minute = True
    running = True
    lose_screen = False
    while running:
        if not lose_screen:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return None, timer_text

            # Update time
            current_time = datetime.now()
            elapsed_time = current_time - start_time
            # Check if the minute should be added
            if elapsed_time.seconds % 10 == 0 and add_minute:
                start_time += timedelta(minutes=1)
                add_minute = False  # Set the flag to False to indicate that the minute has been added
            elif elapsed_time.seconds % 10 != 0:
                add_minute = True  # Reset the flag if the condition is no longer true
            # Adjust time based on key pickup
            if player.add_time:
                start_time += timedelta(minutes=1)  # Add a minute to the start time
                player.add_time = False  # Reset add_time to False
            elif player.sub_time:
                start_time -= timedelta(minutes=1)  # Subtract a minute from the start time
                player.sub_time = False  # Reset sub_time to False

            # Render time
            timer_text = start_time.strftime("%H:%M")

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                player.move(-2, 0)
                player.direction = 'left'
            if key[pygame.K_RIGHT]:
                player.move(2, 0)
                player.direction = 'right'
            if key[pygame.K_UP]:
                player.move(0, -2)
                player.direction = 'up'
            if key[pygame.K_DOWN]:
                player.move(0, 2)
                player.direction = 'down'

            for key in keys:
                if player.rect.colliderect(key.rect):
                    if key.key_type == 'greenapple':
                        player.add_time = True  # Set add_time to True when picking up a green apple
                    elif key.key_type == 'redapple':
                        player.sub_time = False  # Set add_time to False when picking up a red apple
                    key.rect.x = 2000
                    key.rect.y = 2000
                    player.counter -= 1

            if player.rect.colliderect(escape.rect):
                return (True, timer_text)
            screen.fill(DARK_GRAY)
            for wall in walls:
                pygame.draw.rect(screen, (DARK_GRAY), wall.rect)
                all_sprites_list.add(wall)
            for key in keys:
                pygame.draw.rect(screen,(DARK_GRAY), key.rect)
                all_sprites_list.add(key)

            player.draw(screen)

            all_sprites_list.draw(screen)

            # Render text
            timer_surface = font.render(timer_text, True, (255, 255, 255))
            screen.blit(timer_surface, (1050 - timer_surface.get_width() // 2, 20))

            if timer_text == '09:00':
                lose_screen = True
            pygame.display.update()
            clock.tick(100)
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return None, timer_text
            screen.blit(lose_screen1, (0, 0))
            screen.blit(lose_screen2, (0, 200))
            screen.blit(lose_screen3 , (380, 150))
            pygame.display.update()
    return (False, timer_text)
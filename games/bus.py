import pygame
import random
from pygame.locals import *
def play():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Set up the screen
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chase the Bus")

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 40, 40)
            self.image = pygame.image.load("sprites/maze/player.png") 
            self.image = pygame.transform.scale(self.image, (40, 40))
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

            # for key in keys:
            #     if self.rect.colliderect(key.rect):
            #         if key.key_type == 'greenapple':
            #             self.add_time = True  # Set add_time to True when picking up a green apple
            #         elif key.key_type == 'redapple':
            #             self.sub_time = True  # Set add_time to False when picking up a red apple
            #         key.rect.x = 2000
            #         key.rect.y = 2000
            #         self.counter -= 1


        def draw(self, screen, camera_offset):
            if self.direction == 'left':
                rotated_image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                rotated_image = pygame.transform.rotate(self.image, -90)
            elif self.direction == 'down':
                rotated_image = pygame.transform.rotate(self.image, 180)
            else:
                rotated_image = self.image

            screen.blit(rotated_image, self.rect.move(camera_offset))

    class Bus:
        def __init__(self, x, y):
            self.image = pygame.Surface((100, 50))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.speed = 2

        def move(self):
            self.rect.move_ip(self.speed, 0)

        def draw(self, screen, camera_offset):
            screen.blit(self.image, self.rect.move(camera_offset))

    class Obstacle:
        def __init__(self, x, y):
            self.image = pygame.Surface((20, 20))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = 3

        def move(self):
            self.rect.move_ip(-self.speed, 0)

        def draw(self, screen, camera_offset):
            screen.blit(self.image, self.rect.move(camera_offset))

    class Wall(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
            self.image = pygame.image.load(f"sprites/maze/flower.png")
        def draw(self, screen, camera_offset):
            screen.blit(self.image, self.rect.move(camera_offset))

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
        def draw(self, screen, camera_offset):
            screen.blit(self.image, self.rect.move(camera_offset))

    # Create player and bus
    bus = Bus(SCREEN_WIDTH // 2, 0)

    # Obstacles (People)
    obstacles = []
    obstacle_spawn_rate = 60
    obstacle_counter = 0

    all_sprites_list = pygame.sprite.Group()
    keys = []
    walls = [] 
    player = Player() 
    level =  [
    "                                                       ",
    "                                                       ",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW   WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "W                                                     W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ]
    
    levels = []
    for i in range(0, 15):
        levels.append(level)

    # Parse the level string above. W = wall, E = exit
    x = y = 0
    dx = 0
    for level in levels:
        for row in level:
            for col in row:
                if col == "W":
                    Wall((x, y))
                x += 20 + dx
            y += 20
            x = 0 + dx
        dx += 1100 
        
    # Determine the number of keys of each type
    num_gold_keys = 3
    num_silver_keys = 3

    # Keep track of available positions to place keys
    available_positions = []

    # Iterate through the level to find available positions
    for level in levels:
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

    # Camera
    camera_offset = [0, 0]

    clock = pygame.time.Clock()
    # Game loop
    running = True
    knockback_timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        key = pygame.key.get_pressed()
        if key[K_UP] and knockback_timer <= 0 and player.rect.top > 0:
            player.move(0, -2)
            player.direction = 'up'
        if key[K_DOWN] and knockback_timer <= 0 and player.rect.bottom < SCREEN_HEIGHT:
            player.move(0, 2)
            player.direction = 'down'
        if key[K_LEFT] and knockback_timer <= 0:
            player.move(-2, 0)
            player.direction = 'left'
        if key[K_RIGHT] and knockback_timer <= 0:
            player.move(2, 0)
            player.direction = 'right'

        for key in keys:
            if player.rect.colliderect(key.rect):
                if key.key_type == 'greenapple':
                    player.add_time = True  # Set add_time to True when picking up a green apple
                elif key.key_type == 'redapple':
                    player.sub_time = False  # Set add_time to False when picking up a red apple
                key.rect.x = 2000
                key.rect.y = 2000
                player.counter -= 1

        # Update camera offset to center on the player
        camera_offset[0] = -(player.rect.centerx - SCREEN_WIDTH // 2)
    
        # Move the bus
        bus.move()

        # Update obstacles
        if obstacle_counter % obstacle_spawn_rate == 0:
            spawn_x = SCREEN_WIDTH + random.randint(0, 200)
            spawn_y = random.randint(0, SCREEN_HEIGHT)
            obstacles.append(Obstacle(spawn_x, spawn_y))
        obstacle_counter += 1

        for obstacle in obstacles:
            # Check for collision with player
            if player.rect.colliderect(obstacle.rect):
                # Push the player back if it collides with the obstacle
                player.move(-obstacle.speed, 0)
                # Start the knockback timer
                knockback_timer = 1  # 1 second at 60 FPS
            else:
                obstacle.move()
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)

        # Decrease knockback timer and restore player control if knockback period is over
        if knockback_timer > 0:
            knockback_timer -= 1

        # Draw everything
        screen.fill(WHITE)
        
        for wall in walls:
            wall.draw(screen, camera_offset)
        for key in keys:  
            key.draw(screen, camera_offset)

        all_sprites_list.draw(screen)
        bus.draw(screen, camera_offset)
        player.draw(screen, camera_offset)
        for obstacle in obstacles:
            obstacle.draw(screen, camera_offset)

        pygame.display.flip()
        clock.tick(60)

play()
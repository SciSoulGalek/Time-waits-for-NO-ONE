import pygame
import random
from pygame.locals import *
from datetime import datetime, timedelta
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

    lose_screen1 = pygame.image.load("sprites/final/lose.png")
    lose_screen2 = pygame.image.load("sprites/final/losech.png")
    lose_screen3 = pygame.image.load("sprites/main/yourelateloss.png")

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
            speed = 2
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
        def __init__(self, x, y, max_distance, stop_duration):
            self.image = pygame.image.load('sprites/bus/bus.png')
            self.image = pygame.transform.scale(self.image, (300, 80))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.speed = 4
            self.max_distance = max_distance
            self.stop_duration = stop_duration
            self.distance_traveled = 0
            self.stop_timer = 0
            self.finish = False

        def move(self, player_rect):
            distance_x = self.rect.x - player_rect.x
            distance_y = abs(self.rect.y - player_rect.y)

            if distance_y <= 140 and distance_x > -210 and distance_x < 0:
                self.finish = True
                return self.finish
            else:
                if distance_x < self.max_distance and self.stop_timer <= 1:
                    self.rect.x += self.speed
                    self.distance_traveled += self.speed
                    if self.distance_traveled > 1100:
                        self.stop_timer = self.stop_duration
                        self.distance_traveled = 0

            if self.stop_timer > 0:
                self.stop_timer -= 1

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

    # Create bus
    bus = Bus(SCREEN_WIDTH // 2 - 150, 25, 1100, 120)

    # Obstacles (People)
    obstacles = []
    obstacle_spawn_rate = 60
    obstacle_counter = 0

    font = pygame.font.SysFont('Aries', 40)
    all_sprites_list = pygame.sprite.Group()
    keys = []
    walls = [] 
    player = Player() 
    
    # Define the regions where blocks can appear (in this case, a strip in the middle of the level)
    block_region_start = 16
    block_region_end = 30

    # Determine the number of keys of each type
    num_gold_keys = 3
    num_silver_keys = 3
    
    # Keep track of available positions to place blocks
    
    for i in range(35):
        Wall((-20, 0 + 20 * i))

    for level_index in range(15):
        available_positions = []
        level = [
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                   WWWWWWWWWWWWWWWWW                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "                   W               W                   ",
        "WWWWWWWWWWWWWWWWWWWW               WWWWWWWWWWWWWWWWWWWW",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "                                                       ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W                                                     W",
        "W                                                     W",
        "W                                                     W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        ]
    
        x_offset = level_index * len(level[0]) * 20  # Calculate the x-offset for each level
        for y, row in enumerate(level):
            for x, col in enumerate(row):
                if col == "W":
                    Wall((x * 20 + x_offset, y * 20))
                if col == ' ' and block_region_start <= y < block_region_end:
                    available_positions.append((x * 20 + x_offset, y * 20))  # Convert grid position to pixel position
    
        # Shuffle the available positions
        random.shuffle(available_positions)

        # Create blocks at randomly selected positions within the central side region
        for _ in range(10):  # Adjust the number of blocks as needed
            if available_positions:
                pos = available_positions.pop()
                print(f"Creating block at position {pos}")
                # Create block at pos
                Wall(pos)

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

    #Start time
    start_time = datetime.strptime("08:30", "%H:%M")
    add_minute = True
    lose_screen = False

    # Game loop
    running = True
    knockback_timer = 0
    while running:
        if not lose_screen:
            for event in pygame.event.get():
                if event.type == QUIT:
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
                        player.sub_time = True  # Set add_time to False when picking up a red apple
                    key.rect.x = 2000
                    key.rect.y = 2000
                    player.counter -= 1

            # Update camera offset to center on the player
            camera_offset[0] = -(player.rect.centerx - SCREEN_WIDTH // 2)

            # Move the bus
            bus.move(player.rect)

            if bus.finish:
                return True, timer_text

            # Update obstacles
            if obstacle_counter % obstacle_spawn_rate == 0:
                spawn_x = SCREEN_WIDTH + player.rect.x + random.randint(0, 200)
                spawn_y = random.randint(320, 600)
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

            # Render text
            timer_surface = font.render(timer_text, True, (255, 255, 255))
            screen.blit(timer_surface, (1050 - timer_surface.get_width() // 2, 20))

            if timer_text == '09:00':
                lose_screen = True
            pygame.display.flip()
            clock.tick(60)
        
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False, timer_text
            screen.blit(lose_screen1, (0, 0))
            screen.blit(lose_screen2, (0, 200))
            screen.blit(lose_screen3 , (380, 150))
            pygame.display.update()

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1100, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Bus!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
bus_stop_rect = pygame.Rect(0, 150, 1100, 550)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill('BLUE')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 3
        self.stunned = False
        self.stun_duration = 30  # Stun duration in frames

    def update(self, keys):
        if self.stunned:
            self.stun_duration -= 1
            if self.stun_duration <= 0:
                self.stunned = False
                self.stun_duration = 30  # Reset stun duration
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

            # Ensure player stays within bus stop boundaries
            self.rect.left = max(self.rect.left, bus_stop_rect.left)
            self.rect.right = min(self.rect.right, bus_stop_rect.right)
            self.rect.top = max(self.rect.top, bus_stop_rect.top)
            self.rect.bottom = min(self.rect.bottom, bus_stop_rect.bottom)

# Bus
bus_width, bus_height = 450, 120
bus_x, bus_y = 0, 15
bus_speed = 7
bus_stop_duration = 180  # Bus stop duration in frames
bus_stopped = False
bus_stop_timer = 0

# People
people_width, people_height = 30, 30
people_speed = 1
people = []
for _ in range(30):
    person = pygame.Rect(random.randint(50, screen_width - 50),
                         random.randint(300, 600),
                         people_width, people_height)
    direction = random.choice([-1, 1])
    people.append((person, direction, random.randint(60, 180), random.randint(0, 3)))  # (person_rect, direction, change_direction_timer, vertical_speed)

player = Player(50, screen_height - 60)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    if not bus_stopped:
        # Update bus position
        bus_x += bus_speed
        if bus_x > screen_width:
            bus_x = -bus_width

        # Check if the bus should stop
        if (screen_width - bus_width) // 2 - 3 <= bus_x and bus_x <= (screen_width - bus_width) // 2 + 3:
            bus_stopped = True
            bus_stop_timer = bus_stop_duration

    if bus_stopped:
        # Update people to run towards the bus immediately after it stops
        for i, (person, _, _, _) in enumerate(people):
            direction = -1 if bus_x + bus_width // 2 < person.x else 1
            vertical_speed = -1 if bus_y + bus_height // 2 < person.y else 1
            people[i] = (person, direction, random.randint(60, 180), vertical_speed)
        
        bus_center = (bus_x + bus_width // 2, bus_y + bus_height // 2)
        teleport_radius = 100  # Adjust the teleportation radius as needed
        for i, (person, _, _, _) in enumerate(people):
            person_center = (person.x + person.width // 2, person.y + person.height // 2)
            distance = ((person_center[0] - bus_center[0])**2 + (person_center[1] - bus_center[1])**2)**0.5
            if distance <= teleport_radius:
                # Teleport the person to a random position on the screen border
                side = random.choice(['left', 'right', 'bottom'])
                if side == 'left':
                    person.left = 0
                elif side == 'right':
                    person.right = screen_width
                elif side == 'bottom':
                    person.bottom = screen_height
                direction = random.choice([-1, 1])  # Change direction randomly
                people[i] = (person, direction, random.randint(60, 180), random.randint(0, 3))  # Update the person in the list

        # Bus is stopped
        bus_stop_timer -= 1
        if bus_stop_timer <= 0:
            bus_stopped = False

    # Update people position and direction
    for i, (person, direction, change_direction_timer, vertical_speed) in enumerate(people):
        person.x += direction * random.randint(0, 3)
        if person.left < bus_stop_rect.left:
            person.left = bus_stop_rect.left
            direction = 1
        elif person.right > bus_stop_rect.right:
            person.right = bus_stop_rect.right
            direction = -1

        # Change direction randomly over time
        change_direction_timer -= 1
        if change_direction_timer <= 0:
            direction = random.choice([-1, 1])
            change_direction_timer = random.randint(60, 180)
        people[i] = (person, direction, change_direction_timer, vertical_speed)

        # Move people up and down
        person.y += vertical_speed
        if person.top < bus_stop_rect.top:
            person.top = bus_stop_rect.top
            vertical_speed = random.randint(0, 3)
        elif person.bottom > bus_stop_rect.bottom:
            person.bottom = bus_stop_rect.bottom
            vertical_speed = -random.randint(0, 3)
        people[i] = (person, direction, change_direction_timer, vertical_speed)

        # Check for collisions between player and people
        if player.rect.colliderect(person):
            player.stunned = True

    # Check if the player caught the bus
    if player.rect.colliderect(bus_stop_rect):
        if bus_x - bus_width >= screen_width:
            bus_x = 0 - bus_width

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, 'gray', bus_stop_rect)
    screen.blit(player.image, player.rect)
    pygame.draw.rect(screen, RED, (bus_x, bus_y, bus_width, bus_height))
    if bus_stopped:
        pygame.draw.circle(screen, (0, 255, 0), (bus_x + bus_width // 2, bus_y + bus_height // 2), 5)  # Green circle at bus stop position
    for person, _, _, _ in people:
        pygame.draw.rect(screen, RED, person)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

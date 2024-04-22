import pygame, sys
import choose_menu, bus, maze

#Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time waits for NO ONE")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

background = pygame.image.load("sprites/main/room/room1.png")
font = pygame.font.Font(None, 36)

button_size = (225, 75)
start_sprite = pygame.image.load("sprites/main/start.png")
start_sprite = pygame.transform.scale(start_sprite, button_size)
options_sprite = pygame.image.load("sprites/main/options.png")
options_sprite = pygame.transform.scale(options_sprite, button_size)
quit_sprite = pygame.image.load("sprites/main/quit.png")
quit_sprite = pygame.transform.scale(quit_sprite, button_size)

# Darken the background image
dark_overlay = pygame.Surface((WIDTH, HEIGHT))
darkness = 200
dark_overlay.set_alpha(darkness)  # Set transparency (0 = fully transparent, 255 = fully opaque)
dark_overlay.fill((0, 0, 0))  # Fill with black color

win = False

timer: str = ''
# Button class
class Button:
    def __init__(self, source, x, y, action):
        self.x = x
        self.y = y
        self.source = source
        self.rect = self.source.get_rect(topleft=(self.x, self.y))
        self.action = action

    def draw(self, surface):
        surface.blit(self.source, (self.x, self.y))

    def check_hover(self, pos):
        return self.rect.collidepoint(pos)

# Menu class
class Menu:
    def __init__(self):
        self.buttons = []
        self.add_button(start_sprite, WIDTH // 2 - button_size[0] // 2, 400, 1)
        self.add_button(options_sprite, WIDTH // 2 - button_size[0] // 2, 500, 2)
        self.add_button(quit_sprite, WIDTH // 2 - button_size[0] // 2, 600, 3)

    def add_button(self, source, x, y, action):
        button = Button(source, x, y, action)
        self.buttons.append(button)

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.check_hover(pygame.mouse.get_pos()):
                    return button.action
        return None

# Main menu loop
def main_menu():
    menu = Menu()
    running = True

    while running:
        if pygame.display.get_init():  # Check if Pygame display is initialized
            screen.blit(background, (0, 0))
            # Draw the dark overlay on top
            screen.blit(dark_overlay, (0, 0))
            menu.draw(screen)
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = menu.handle_event(event)
            if action == 1:
                chose = choose_menu.activate(darkness)
                if chose == 1:
                    bus.play()
                elif chose == 2:
                    win, timer = maze.play()
                    if win:
                        # win, timer = earthquake.play(timer)
                        pass
            elif action == 2:
                print("Options button clicked")
                # Add your options logic here
            elif action == 3:
                pygame.quit()
                sys.exit()

# Game function
def start_game():
    # Game logic and rendering
    print("Starting game...")
    # Simulating game end
    print("Game over.")
    return_to_main_menu()

# Options menu function
def options_menu():
    # Options menu logic and rendering
    print("Options menu...")
    return_to_main_menu()

# Return to main menu function
def return_to_main_menu():
    main_menu()

# Run main menu
main_menu()
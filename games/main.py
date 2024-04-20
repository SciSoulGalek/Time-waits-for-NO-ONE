import pygame, sys
import choose_menu, bus, maze

#Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KBTU GO!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        return self.rect.collidepoint(pos)

# Menu class
class Menu:
    def __init__(self):
        self.buttons = []
        self.add_button("Start", WIDTH // 2 - 100, 200, 200, 50, GREEN, RED, 1)
        self.add_button("Options", WIDTH // 2 - 100, 300, 200, 50, GREEN, RED, 2)
        self.add_button("Quit", WIDTH // 2 - 100, 400, 200, 50, GREEN, RED, 3)

    def add_button(self, text, x, y, width, height, color, hover_color, action):
        button = Button(text, x, y, width, height, color, hover_color, action)
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
    choosing_game = False
    while running:
        if pygame.display.get_init():  # Check if Pygame display is initialized
            screen.fill(WHITE)
            menu.draw(screen)
            time: int = 30
            text = str(time)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = menu.handle_event(event)
            if action == 1:
                chose = choose_menu.activate(text)
                if chose == 1:
                    bus.play(text)
                elif chose == 2:
                    maze.play()
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
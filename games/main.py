import pygame, sys
import choose_menu, bus, maze, earthquake, alien

#Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time waits for NO ONE")
# Load icon image
icon_sprite = pygame.image.load("sprites/main/mainlogo.png")
icon_sprite = pygame.transform.scale(icon_sprite, (400, 400))
pygame.display.set_icon(icon_sprite)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Win screen 
win_screen1 = pygame.image.load("sprites/final/winch.png")
win_screen2 = pygame.image.load("sprites/final/win.png")
win_screen3 = pygame.image.load("sprites/main/youmadeitwin.png")

background = pygame.image.load("sprites/main/room/room1.png")
font = pygame.font.Font(None, 36)

button_size = (225, 75)
start_sprite = pygame.image.load("sprites/main/start.png")
start_sprite = pygame.transform.scale(start_sprite, button_size)
options_sprite = pygame.image.load("sprites/main/options.png")
options_sprite = pygame.transform.scale(options_sprite, button_size)
quit_sprite = pygame.image.load("sprites/main/quit.png")
quit_sprite = pygame.transform.scale(quit_sprite, button_size)
logo_sprite = pygame.image.load("sprites/main/mainlogo.png")
logo_sprite = pygame.transform.scale(logo_sprite, (450, 450))
skip = pygame.image.load("sprites/main/skip.png")
skip_rect = skip.get_rect(topleft = (900, 600))

clocks = [906, '906-2', 906, 905, 905, 905, 904, 904, 904, 903, 903, 902, 902, 901, 901, 900, 858, 856, 854, 852, 850, 848, 846, 844, 842, 840, 839, 838, 837, 836, 836, 835, 835, 834, 834, 833, 833, 833, 832, 832, 832, 831, 831, 831, 830, '830-2', 830]
animation = []
for clock_value in clocks:
    filename = f"sprites/clock/{clock_value}.png"
    clock = pygame.image.load(filename)
    animation.append(clock)

# Darken the background image
dark_overlay = pygame.Surface((WIDTH, HEIGHT))
darkness = 200
dark_overlay.set_alpha(darkness)  # Set transparency (0 = fully transparent, 255 = fully opaque)
dark_overlay.fill((0, 0, 0))  # Fill with black color

win1 = False
win2 = False
win3 = False

timer_text: str = ''
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

def back_in_time(timer):
    while True:    
        for event in pygame.event.get():  
            if event.type == TIMER:
                timer += 1
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if the mouse click is within the back button
                if skip_rect.collidepoint(pos):
                    return
        if timer < len(clocks):
                screen.blit(animation[timer], (0, 0))
        screen.blit(skip, (900, 600))
        pygame.display.update()

timer = 0
TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, 250)
cutscene = False

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
            screen.blit(logo_sprite, (WIDTH // 2 - 225, -25))
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = menu.handle_event(event)
            if action == 1:
                chose = choose_menu.activate(darkness)
                if chose == 1:
                    win1, timer_text = bus.play()
                elif chose == 2:
                    win1, timer_text = maze.play()

                if win1:
                    win2, timer_text = earthquake.play(timer_text)
                    if win2:
                        win3, timer_text = alien.play(timer_text)
                        if win3:
                            screen.blit(win_screen1, (0, 0))
                            screen.blit(win_screen2, (0, 200))
                            screen.blit(win_screen3, (0, 200)) #win screen
                        else:
                            back_in_time(timer)
                    else:
                        back_in_time(timer)
                else:
                    back_in_time(timer)
                    
            elif action == 2:
                print("Options button clicked")
                # Add your options logic here
            elif action == 3:
                pygame.quit()
                sys.exit()

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
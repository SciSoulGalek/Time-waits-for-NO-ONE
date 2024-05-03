import pygame, sys
import choose_menu, bus, maze, earthquake, alien

#Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sound/main/mainminus.wav')
pygame.mixer.music.play(-1)
alarm = pygame.mixer.Sound('sound/other/alarmclock.wav')
volume = 1

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
win_screen1 = pygame.image.load("sprites/final/win.png")
win_screen2 = pygame.image.load("sprites/final/winch.png")
win_screen3 = pygame.image.load("sprites/main/youmadeitwin.png")

background = pygame.image.load("sprites/main/room/room1.png")

# Create a font object
font = pygame.font.Font("fonts/superfont.ttf", 22)  # Adjust the font and size as needed
font_big = pygame.font.Font(None, 190)  # Adjust the font and size as needed

button_size = (225, 75)
main_menu_button = pygame.image.load("sprites/choose_menu/main_menu.png")
main_menu_button = pygame.transform.scale(main_menu_button, (150, 50))
main_menu_button_rect = main_menu_button.get_rect(topleft = (50, 50))
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

clocks = [906, '906-2', 906, 905, 905, 905, 904, 904, 904, 903, 903, 902, 902, 901, 901, 900, 858, 856, 854, 852, 850, 848, 846, 844, 842, 840, 839, 838, 837, 836, 836, 835, 835, 834, 834, 833, 833, 833, 832, 832, 832, 831, 831, 831, 830]
clocks2 = ['830-2', 830, '830-2', 830, '830-2', 830, '830-2', 830, '830-2', 830]
animation = []
animation2 = []
for clock_value in clocks:
    filename = f"sprites/clock/{clock_value}.png"
    clock = pygame.image.load(filename)
    animation.append(clock)

for clock_value in clocks2:
    filename = f"sprites/clock/{clock_value}.png"
    clock = pygame.image.load(filename)
    animation2.append(clock)

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
    alarm_played = False
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
                    alarm.stop()
                    play_music() 
                    return
        if timer < len(clocks):
                screen.blit(animation[timer], (0, 0))
        else:
            if not alarm_played:  # Check if alarm has not been played yet
                if (timer - 44) < len(clocks2):
                    screen.blit(animation2[timer - 44], (0, 0))
                play_alarm()
                pygame.mixer.music.load('sound/main/mainminus.wav')
                alarm_played = True
        screen.blit(skip, (900, 600))
        pygame.display.update()

def win_screen():
    winning = True
    while winning:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                winning = False
        screen.blit(win_screen1, (0, 0))
        screen.blit(win_screen2, (0, 200))
        screen.blit(win_screen3, (0, 200)) #win screen
        pygame.display.update()
    play_music()
    return

def play_music():
    pygame.mixer.music.load('sound/main/mainminus.wav')
    pygame.mixer.music.play(-1)
    # pygame.mixer.music.set_volume()

def play_alarm():
    alarm.play()

timer = 0
TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, 250)
cutscene = False

# Main menu loop
def main_menu():
    global win1
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
                pygame.mixer.music.pause()
                pygame.mixer.music.rewind()
            else:
                pygame.mixer.music.unpause()
            if action == 1:
                chose = choose_menu.activate(darkness)
                if chose == 1:
                    win1, timer_text = bus.play()
                elif chose == 2:
                    win1, timer_text = maze.play()
                else:
                    win1 = None

                if win1 == True:
                    win2, timer_text = earthquake.play(timer_text)
                    if win2:
                        win3, timer_text = alien.play(timer_text)
                        if win3:
                            win_screen()
                            continue
                        elif win3 == None:
                            play_music()
                            continue
                        else:
                            back_in_time(timer)
                    elif win2 == None:
                        play_music()
                        continue
                    else:
                        back_in_time(timer)
                elif win1 == None:
                    play_music()
                    continue
                else:
                    back_in_time(timer)
                    
            elif action == 2:
                print("Options button clicked")
                options_menu()
                # Add your options logic here
            elif action == 3:
                pygame.quit()
                sys.exit()

# Options menu function
def options_menu():
    while True:
        global volume
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                return None, timer_text
            elif event.type == pygame.KEYDOWN:
                #volume
                if event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if the mouse click is within the back button
                if main_menu_button_rect.collidepoint(pos):
                    return
        
        screen.blit(background, (0, 0))
        # Draw the dark overlay on top
        screen.blit(dark_overlay, (0, 0))
        # Draw overlay on top
        volume_text = font_big.render(f'Volume: {int(volume * 100)}', True, (255, 255, 255)) 
        screen.blit(volume_text, (200, HEIGHT // 2))
        screen.blit(main_menu_button, (50, 50))
        pygame.display.update()

# Run main menu
main_menu()
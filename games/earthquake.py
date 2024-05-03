import pygame
from pygame.locals import *
from datetime import datetime, timedelta
def play(timer_text):  
    pygame.init()

    screen_width = 1100
    screen_height = 700

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Time-waits-for-no-one')
    animation = []
    for i in range(1,10):
            st = pygame.image.load(f'sprites/earthquake/street{i%3 + 1}.png')
            animation.append(st)
    for i in range(1,13):
        er = pygame.image.load(f'sprites/earthquake/earthquake{i}.png')
        animation.append(er)

    # Load the "co" image
    comment = pygame.image.load('sprites/earthquake/street.png')
    font = pygame.font.Font("fonts/superfont.ttf", 19)  # Adjust the font and size as needed
    text_surface = font.render("Shaking. Gap. Darkness. Julia falls into the pit.", True, (255, 255, 255))  # Adjust text and color as needed
    text_position = (150, 575)  # Adjust the position as needed

    # Display the image
    pygame.display.flip()
    animation.append(comment)

    # scrolling 
    scroll_th= 200
    scroll=[0,0]
    #define game variables
    tile_size = 55
    game_over=0

    #sound
    bgsound = pygame.mixer.Sound("sound/earthquake/bc.mp3")
    de=pygame.mixer.Sound("sound/earthquake/de.mp3")
    earthqu=pygame.mixer.Sound("sound/earthquake/quake.mp3")
    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            #draw button
            screen.blit(self.image, self.rect)

            return action
    class Player():
        def __init__(self, x, y):
            self.images_r=[]
            self.images_l=[]
            self.index=0
            self.count=0
            self.direction=0
            for i in range(1,4):
                imgr = pygame.image.load(f'sprites/earthquake/{i}.png')
                imgr = pygame.transform.scale(imgr, (30, 60))
                imgl = pygame.transform.flip(imgr,True,False)
                self.images_r.append(imgr)
                self.images_l.append(imgl)

            self.image=self.images_r[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()


            self.vel_x = 0  # Initialize horizontal velocity
            self.vel_y = 0
            self.jumped = False
            self.in_air = True

        
        def update(self, game_over):
            dx = 0  # Initialize horizontal movement
            dy = 0  # Initialize vertical movement
            wc = 5  # Animation counter limit

            # Check key presses
            if game_over == 0:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                    self.vel_y = -16
                    self.jumped = True
                if not key[pygame.K_SPACE]:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    if self.rect.x > 0:  # Check if player is not at the left edge
                        dx -= 3   # Move left
                        self.count += 1
                        self.direction = -1
                elif key[pygame.K_RIGHT]:
                    # Check if player is not at the right edge
                        dx += 3  # Move right
                        self.count += 1
                        self.direction = 1
                else:
                    self.vel_x = 0  # No horizontal movement if no key pressed
                if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                    self.count = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_r[self.index]
                    elif self.direction == -1:
                        self.image = self.images_l[self.index]

                # Apply animation
                if self.count > wc:
                    self.count = 0
                    self.index += 1
                    if self.index >= len(self.images_r):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_r[self.index]
                    elif self.direction == -1:
                        self.image = self.images_l[self.index]

                # Apply gravity
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                # collision
                self.in_air = True
                for tile in world.tile_list:
                    # y direction
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    # check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        # check if below the ground i.e. jumping
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        # check if above the ground i.e. falling
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                if pygame.sprite.spritecollide(self, lava_group, False):
                    game_over = -1
                    de.play()
            
            # update player coordinates with scrolling adjustment
            self.rect.x += dx
            self.rect.y += dy 
            
            # Draw player onto screen with scrolling adjustment
            screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
            
            return game_over

    class World():
        def __init__(self, data):
            self.tile_list = []
            self.grass_tiles = []

            #load images
            dirt_img = pygame.image.load('sprites/earthquake/dirt.png')
            grass_img = pygame.image.load('sprites/earthquake/grass.png')
           

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size -scroll[0]
                        img_rect.y = row_count * tile_size-scroll[1]
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 12:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size//2))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size-scroll[0]
                        img_rect.y = row_count * tile_size-scroll[1]
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size//2))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size-scroll[0]
                        img_rect.y = row_count * tile_size-scroll[1]
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                        self.grass_tiles.append([img_rect, 1])
                    if tile == 4:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size//2))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size-scroll[0]
                        img_rect.y = row_count * tile_size-scroll[1]
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 7:
                        coin = Coin(col_count * (tile_size-scroll[0]) + (tile_size // 2), row_count * (tile_size-scroll[1]) + (tile_size // 2))
                        coin_group.add(coin)
                    if tile == 8:
                        e = Enemy(col_count * (tile_size-scroll[0]) + (tile_size // 2), row_count * (tile_size-scroll[1]) + (tile_size // 2))
                        enemy_group.add(e)
                    if tile == 9:
                        exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        exit_group.add(exit)
                    if tile == 3:
                        lave=lava(col_count*(tile_size-scroll[0]),row_count*(tile_size-scroll[1]) )
                        lava_group.add(lave)
                    
                    col_count += 1
                row_count += 1

        def update(self):
            # Move the grass tiles left and right
            for grass in self.grass_tiles:
                grass_rect, direction = grass
                if direction == 1:  # Move right
                    grass_rect.x += 1  # Change the value to adjust the speed of movement
                    # Check if the grass tile is about to go out of bounds
                    if grass_rect.right > 1500:
                        grass[1] = -1  # Change direction to left
                else:  # Move left
                    grass_rect.x -= 1  # Change the value to adjust the speed of movement
                    # Check if the grass tile is about to go out of bounds
                    if grass_rect.left < 200:
                        grass[1] = 1  # Change direction to right

        def draw(self):
            for tile in self.tile_list:
                adjusted_rect = tile[1].move(-scroll[0], -scroll[1])
                screen.blit(tile[0], adjusted_rect)
                
    class lava(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []  # List to hold lava images
            self.index = 0  # Index for the current lava image
            self.animation_time = 500  # Time between each frame change (in milliseconds)
            self.last_update = pygame.time.get_ticks()  # Last time the frame was changed
            for i in range(1, 3):  # Assuming you have two lava images named lava1.png and lava2.png
                img = pygame.image.load(f'sprites/earthquake/lava{i}.png')
                self.images.append(pygame.transform.scale(img, (tile_size, tile_size)))
            self.image = self.images[self.index]  # Set initial image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            # Check if it's time to change the frame
            if pygame.time.get_ticks() - self.last_update > self.animation_time:
                self.last_update = pygame.time.get_ticks()  # Update last update time
                self.index += 1  # Move to the next frame
                if self.index >= len(self.images):  # If reached the end of the animation, start over
                    self.index = 0
                self.image = self.images[self.index]  # Update the current image

            # You can add any other update logic here, such as movement or collision detection

    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('sprites/earthquake/redapple.png')
            self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
            self.rect = self.image.get_rect()
            # Adjust position based on scrolling offset
            self.rect.x = x - scroll[0]
            self.rect.y = y - scroll[1]

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('sprites/earthquake/greenapple.png')
            self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
            self.rect = self.image.get_rect()
            # Adjust position based on scrolling offset
            self.rect.x = x - scroll[0]
            self.rect.y = y - scroll[1]

    class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('sprites/earthquake/door.png')
            self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y




    world_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 7, 7, 0 ,0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 8, 8, 4, 4, 4, 0 ,0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 4, 4, 4, 0, 0, 0, 0, 4, 0, 0, 4, 4, 0, 8, 8, 0, 0, 0, 0,0, 0, 0, 2, 2, 0, 0, 0, 0 ,4, 4, 1, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 4, 0 ,0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0,0, 8, 8, 7, 0, 0, 0, 0, 0 ,8, 0, 0, 0, 0, 4],
        [0, 0, 0, 4, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 2, 2, 0, 0,0, 0, 4, 4, 0, 0, 0, 4, 4 ,4, 0, 0, 0, 4, 0],
        [0, 4, 4, 0, 0, 0, 0, 0, 0 ,0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 4, 0,4, 0, 4, 4, 4, 4, 0, 0, 2 ,0, 4, 4, 4, 0, 0],
        [0, 7, 7, 0, 0, 0, 7, 8, 4 ,4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 7, 8, 0, 0, 0, 7, 7, 7, 4,0, 8, 7, 7, 0, 0, 0, 0, 2 ,2, 0, 0, 0, 0, 0],
        [0, 4, 4, 0, 0, 0, 4, 4, 0 ,0, 8, 8, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 4, 4, 4, 0, 0, 4, 4, 4, 0, 0, 7, 0, 0 ,0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 8, 0, 0 ,0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 2,2, 0, 0, 0, 0, 0, 0, 4, 0 ,8, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 4, 0, 0 ,0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 4, 4, 4, 0, 0, 0 ,4, 0, 4, 0, 0, 0],
        [0, 12,12 ,12, 0, 0, 0, 4, 0 ,4, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0 ,2, 2, 2, 0, 0, 0], 
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ,3 ,3 , 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,3] 
    ]

    player = Player(100, screen_height - 130)
    lava_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    world = World(world_data)



    fps=30
    clock = pygame.time.Clock()  # Create a clock object to control frame rate


    lose_screem1=pygame.image.load("sprites/earthquake/burned .png")
    lose_screem2=pygame.image.load("sprites/earthquake/burnedch.png")
    lose_screem3=pygame.image.load("sprites/earthquake/yourelateloss.png")
    late_screen1 = pygame.image.load("sprites/final/lose.png")
    late_screen2 = pygame.image.load("sprites/final/losech.png")
    late_screen3 = pygame.image.load("sprites/main/yourelateloss.png")


    background_image = pygame.image.load("sprites/earthquake/lavabg.png")
    ufo_image = pygame.image.load("sprites/earthquake/ufo.png")
    background_image = pygame.transform.scale(background_image, (1100, 700))

    font = pygame.font.SysFont(None, 36)  # Define font for the timer

    #buttoms 
    exit_img=pygame.image.load("sprites/earthquake/door.png")
    exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

    #skip and dark 
    skip = pygame.image.load("sprites/earthquake/skip.png")
    skip_rect = skip.get_rect(topleft = (950, 0))


    # Add these variables before the game loop
    bg_x = 0
    bg_y = 0

    #curscenetime
    timer = 0
    TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER, 350)
    #curscene
    cutscene = True
    eart_sound_played = False
    text_shown = False

    start_time = datetime.strptime(timer_text, "%H:%M")
    add_minute = True
    run = True
    late_screen = False
    lose_screen = False

  

    # Inside the game loop
    while run:
        if cutscene:
            for event in pygame.event.get():  
                if event.type == TIMER:
                    timer += 1
                if event.type == pygame.QUIT:
                    return False, timer_text
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Check if the mouse click is within the back button
                    if skip_rect.collidepoint(pos):
                        bgsound.play(-1)
                        earthqu.stop()
                        cutscene = False
            if not eart_sound_played:
                earthqu.play()  # Play the eart sound
                eart_sound_played = True 

            if timer < 22:
                screen.blit(animation[timer], (0, 0))
            else:
                if not text_shown:
                    screen.blit(text_surface, text_position)
                    text_shown = True
            screen.blit(skip, (950, 0))
            pygame.display.update()    
        elif late_screen:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False, timer_text
            bgsound.stop()
            screen.blit(late_screen1, (0, 0))
            screen.blit(late_screen2, (0, 200))
            screen.blit(late_screen3 , (380, 150))
            pygame.display.update()
        elif lose_screen:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False, timer_text
            bgsound.stop()
            screen.blit(lose_screem1, (0, 0))
            screen.blit(lose_screem2, (0, 200))
            screen.blit(lose_screem3 , (380,150))
            pygame.display.update()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Clear the screen
            screen.blit(background_image, (0, 0))
            screen.blit(ufo_image,(0,0))
            
            # Update player
            game_over = player.update(game_over)

            # Update scrolling
            scroll[0] += (player.rect.x - scroll[0] - 152) / 20

            # Update world
            world.update()  # Update the positions of the moving grass tiles
            world.draw()

            # Update and draw lava
            lava_group.update()
            lava_group.draw(screen)

        
            for door in exit_group:
                screen.blit(door.image, (door.rect.x - scroll[0], door.rect.y - scroll[1]))
            # Check for collisions
            coin_collisions = pygame.sprite.spritecollide(player, coin_group, True)
            enemy_collisions = pygame.sprite.spritecollide(player, enemy_group, True)
            
            # Update time
            current_time = datetime.now()
            elapsed_time = current_time - start_time
            # Check if the minute should be added
            if elapsed_time.seconds % 10 == 0 and add_minute:
                start_time += timedelta(minutes=1)
                add_minute = False  # Set the flag to False to indicate that the minute has been added
            elif elapsed_time.seconds % 10 != 0:
                add_minute = True  # Reset the flag if the condition is no longer true
            
            # # Adjust time based on key pickup
            # if player.add_time:
            #     start_time += timedelta(minutes=1)  # Add a minute to the start time
            #     player.add_time = False  # Reset add_time to False
            # elif player.sub_time:
            #     start_time -= timedelta(minutes=1)  # Subtract a minute from the start time
            #     player.sub_time = False  # Reset sub_time to False

            # Render time
            timer_text = start_time.strftime("%H:%M")
        

            # Handle collisions with the door
            door_collision = pygame.sprite.spritecollide(player, exit_group, False)
            if door_collision:
                game_over = 1  # Set game_over to a value indicating victory
                bgsound.stop()
            
            # Handle collisions with coins and enemies
            for coin in coin_collisions:
                start_time -= timedelta(minutes=1)  # Add 5 seconds to the remaining time

            for e in enemy_collisions:
                start_time += timedelta(minutes=1)  # Subtract 5 seconds from the remaining time

            # Draw the door sprites

            # Handle collisions with the door

            game_over = player.update(game_over)

            # Update and draw coins and enemies
            if game_over == -1:
                lose_screen = True
            elif game_over == 1:  # Victory condition
                bgsound.stop()
                return (True, timer_text)  # Display the win screen
            else:
                for coin in coin_group:
                    screen.blit(coin.image, (coin.rect.x - scroll[0], coin.rect.y - scroll[1]))
                for e in enemy_group:
                    screen.blit(e.image, (e.rect.x - scroll[0], e.rect.y - scroll[1]))
                timer_surface = font.render(timer_text, True, (255, 255, 255))
                screen.blit(timer_surface, (1050 - timer_surface.get_width() // 2, 20))

            # End game if time runs out
            if timer_text == '09:00':
                late_screen = True
                
                
            pygame.display.update()
            clock.tick(fps)  # Limit frame rate to 30 frames per second
    bgsound.stop()
    return (False, timer_text)



                
                
     

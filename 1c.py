import pygame
from pygame.locals import *

pygame.init()

screen_width = 1100
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# scrolling 
scroll_th= 200

#define game variables
tile_size = 55
game_over=0
bgsound = pygame.mixer.Sound("sound/earthquake/bc.mp3")
bgsound.play()
de=pygame.mixer.Sound("sound/earthquake/de.mp3")
class Player():
    def __init__(self, x, y):
        self.images_r=[]
        self.images_l=[]
        self.index=0
        self.count=0
        self.direction=0
        for i in range(1,5):
            imgr = pygame.image.load(f'sprites/earthquake/png/{i}.png')
            imgr = pygame.transform.scale(imgr, (40, 80))
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

       
    def update(self,game_over):
        dx = 0  # Initialize horizontal movement
        dy = 0  # Initialize vertical movement
        wc = 5  # Animation counter limit

        # Check key presses
        if game_over==0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                if self.rect.x > 0:  # Check if player is not at the left edge
                    dx -= 2  # Move left
                    self.count += 1
                    self.direction=-1
            elif key[pygame.K_RIGHT]:
                if self.rect.x < screen_width - self.width:  # Check if player is not at the right edge
                    dx += 2 # Move right
                    self.count += 1
                    self.direction=1
            else:
                self.vel_x = 0   # No horizontal movement if no key pressed
            if key[pygame.K_LEFT]==False  and key[pygame.K_RIGHT]==False:
                self.count=0
                self.index=0
                if self.direction==1:
                    self.image = self.images_r[self.index]
                if self.direction==-1:
                    self.image = self.images_l[self.index]

            # Apply animation
            if self.count > wc:
                self.count = 0 
                self.index += 1
                if self.index >= len(self.images_r):
                    self.index = 0
                if self.direction==1:
                    self.image = self.images_r[self.index]
                if self.direction==-1:
                    self.image = self.images_l[self.index]


            # Apply gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #collision
            self.in_air = True
            for tile in world.tile_list:
                #y direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False


            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over=-1
                de.play()
            
            
    
            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy
        # Draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,2)
        return game_over


class World():
    def __init__(self, data):
        self.tile_list = []
        self.grass_tiles = []

        #load images
        dirt_img = pygame.image.load('sprites/earthquake/png/dirt.png')
        grass_img = pygame.image.load('sprites/earthquake/png/grass.png')
        lava_img=pygame.image.load('sprites/earthquake/png/lava.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 12:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size//2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size//2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.grass_tiles.append([img_rect, 1])
                if tile == 4:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size//2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile==3:
                    lave=lava(col_count*tile_size,row_count*tile_size )
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
                if grass_rect.right > screen_width:
                    grass[1] = -1  # Change direction to left
            else:  # Move left
                grass_rect.x -= 1  # Change the value to adjust the speed of movement
                # Check if the grass tile is about to go out of bounds
                if grass_rect.left < 0:
                    grass[1] = 1  # Change direction to right

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,(255,255,255),tile[1],2)


class lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("sprites/earthquake/png/lava.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('sprites/earthquake/png/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
    

world_data = [
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 7, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 4, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [12, 12, 12, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,3], 
    
    
]

player = Player(100, screen_height - 130)
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
world = World(world_data)



fps=60
clock = pygame.time.Clock()  # Create a clock object to control frame rate

run = True
lose_screem=pygame.image.load("sprites/earthquake/png/d-2.jpg")
background_image=pygame.image.load("sprites/earthquake/png/hell-2.jpg")

start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
game_time = 120  # 2 minutes in seconds
font = pygame.font.SysFont(None, 36)  # Define font for the timer

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_image, (0, 0))  # Clear the screen

    world.update()  # Update the positions of the moving grass tiles
    world.draw()
    lava_group.draw(screen)
    coin_group.draw(screen)

    
    game_over=player.update(game_over)
    if game_over==-1:
        screen.blit(lose_screem,(0,0))
   
    pygame.draw.line(screen, (255,255,255), (0,scroll_th), (screen_width, scroll_th))

    #Time 
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
    remaining_time = max(game_time - elapsed_time, 0)  # Calculate remaining time

    # collision with coin 
    coin_collisions = pygame.sprite.spritecollide(player, coin_group, True)
    print("Number of coins collided:", len(coin_collisions))
    for coin in coin_collisions:
        # Add 5 seconds to the remaining time
        remaining_time += 5

    # Convert remaining time to minutes and seconds
    minutes = remaining_time // 60
    seconds = remaining_time % 60

   
    
    # Format the time as "MM:SS"
    time_text = "{:02d}:{:02d}".format(minutes, seconds)

    timer_text = font.render(f"Time Left: {time_text}", True, (255, 255, 255))
    if game_over==-1:
        screen.blit(lose_screem,(0,0))
    else:
        screen.blit(timer_text, (20, 20))
    


    # End game if time runs out
    if remaining_time <= 0:
        run = False
    pygame.display.update()
 
    clock.tick(fps)  # Limit frame rate to 30 frames per second

pygame.quit()

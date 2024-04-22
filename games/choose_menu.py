def activate(darkness_number): 
    import pygame
    import sys
    pygame.init()

    WIDTH, HEIGHT = 1100, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Choose a game!")
    font = pygame.font.Font(None, 36)

    background = pygame.image.load("sprites/main/room/room1.png")

    animation = []
    for i in range(12):
        room = pygame.image.load(f"sprites/main/room/room{i % 4 + 1}.png")
        animation.append(room)

    for i in range(9):
        clock = pygame.image.load(f"sprites/clock/clock{i + 1}.png")
        animation.append(clock)
    clockch = pygame.image.load(f"sprites/clock/clock.ch.png")
    animation.append(clockch)

    background_main = pygame.image.load("sprites/alien/square/сквер .png")
    choose_bus = pygame.image.load("sprites/choose_menu/choose_bus.png")
    choose_bus = pygame.transform.scale(choose_bus, (300, 300))
    choose_bus_rect = choose_bus.get_rect(topleft = (150, 200))
    choose_car = pygame.image.load("sprites/choose_menu/choose_car.png")
    choose_car = pygame.transform.scale(choose_car, (300, 300))
    choose_car_rect = choose_car.get_rect(topleft = (650, 200))
    main_menu = pygame.image.load("sprites/choose_menu/main_menu.png")
    main_menu = pygame.transform.scale(main_menu, (150, 50))
    main_menu_rect = main_menu.get_rect(topleft = (50, 50))
    skip = pygame.image.load("sprites/main/skip.png")
    skip_rect = skip.get_rect(topleft = (900, 600))

    # Darken the background image
    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    darkness = darkness_number
    dark_overlay.set_alpha(darkness)  # Set transparency (0 = fully transparent, 255 = fully opaque)
    dark_overlay.fill((0, 0, 0)) 

    timer = 0
    TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER, 250)
    
    cutscene = True
    
    while True:
        if cutscene:
            for event in pygame.event.get():  
                if event.type == TIMER:
                    timer += 1
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Check if the mouse click is within the back button
                    if skip_rect.collidepoint(pos):
                        cutscene = False

            if timer < 22:
                if darkness != 0:
                    darkness -= 1
                    dark_overlay.set_alpha(darkness)
                screen.blit(animation[timer], (0, 0))
                screen.blit(dark_overlay, (0, 0))
                screen.blit(skip, (900, 600))

            # Draw the dark overlay on top
            something = 'This is cutscene'
            something_surface = font.render(something, True, 'white')
            screen.blit(something_surface, (WIDTH // 2, HEIGHT // 2))
            screen.blit(skip, (900, 600))
            pygame.display.update()
        else:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Check if the mouse click is within the back button
                    if main_menu_rect.collidepoint(pos):
                        return 0
                    
                    # Check if the mouse click is within game 1 area
                    if choose_bus_rect.collidepoint(pos):
                        # Start game 1
                        return 1

                    # Check if the mouse click is within game 2 area
                    if choose_car_rect.collidepoint(pos):
                        # Start game 2
                        return 2

            # Draw the game selection screen
            screen.blit(background_main, (0, 0))
            screen.blit(main_menu, (50, 50))
            screen.blit(choose_bus, (150, 200))
            screen.blit(choose_car, (650, 200))
            pygame.display.update()
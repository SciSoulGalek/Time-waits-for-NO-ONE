def activate(text): 
    import pygame
    import sys
    pygame.init()

    WIDTH, HEIGHT = 1100, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Choose a game!")
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the back button
                if 50 <= event.pos[0] <= 150 and 50 <= event.pos[1] <= 100:
                    return

                # Check if the mouse click is within game 1 area
                if 100 <= event.pos[0] <= 300 and 200 <= event.pos[1] <= 300:
                    # Start game 1
                    return 1

                # Check if the mouse click is within game 2 area
                if 400 <= event.pos[0] <= 600 and 200 <= event.pos[1] <= 300:
                    # Start game 2
                    return 2

        # Draw the game selection screen
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), (100, 200, 200, 100))
        pygame.draw.rect(screen, (0, 0, 255), (400, 200, 200, 100))
        pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 50))  # Back button
        text_surface = font.render(text, True, 'BLACK')
        text_rect = text_surface.get_rect()
        screen.blit(text_surface, text_rect)
        pygame.display.update()
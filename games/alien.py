def play(timer):
    import pygame
    import random
    
    # Initialize Pygame
    pygame.init()
    
    # Constants
    WIDTH, HEIGHT = 1100, 700
    RECT_WIDTH = 750
    RECT_HEIGHT = 360
    BG_IMAGE_PATH = 'sprites/alien/square/quiz.png'  # Change this to the path of your image
    QUESTION_FONT_SIZE = 36
    ANSWER_FONT_SIZE = 28
    BUTTON_WIDTH = 350
    BUTTON_HEIGHT = 40
    BUTTON_MARGIN = 20
    QUESTION_DURATION = 10  # 10 seconds per question
    NUM_QUESTIONS = 5  # Number of questions to select
    
    animation = []
    for i in range(20):
        alien = pygame.image.load(f"sprites/alien/square/пришельцы{i + 1}.png")
        animation.append(alien)
    skip = pygame.image.load("sprites/main/skip.png")
    skip_rect = skip.get_rect(topleft = (900, 600))

    # Questions and answers
    questions = [
        {
            "question": "What is the capital of Kazakhstan?",
            "answers": ["A. Astana", "B. Shymkent", "C. Paris", "D. Almaty"],
            "correct_answer": "C. Paris"
        },
        {
            "question": "Where is odd number?",
            "answers": ["A. 3", "B. 4", "C. 5", "D. 7"],
            "correct_answer": "B. 4"
        },
        {
            "question": "Which of these countries is not located in Europe?",
            "answers": ["A. Japan", "B. Kazakhstan", "C. Sweden", "D. Uzbekistan"],
            "correct_answer": "C. Sweden"
        },
        {
            "question": "Which of these animals is not a predator?",
            "answers": ["A. Wolf", "B. Rabbit", "C. Cow", "D. Cat"],
            "correct_answer": "A. Wolf"
        },
        {
            "question": "Which month has 31 days?",
            "answers": ["A. May", "B. June", "C. December", "D. February"],
            "correct_answer": "D. February"
        },
        {
            "question": "What did Leo Tolstoy write?",
            "answers": ["A. War and Peace", "B. Martin Eden", "C. Anna Karenina", "D. Sunday"],
            "correct_answer": "B. Martin Eden"
        },
        {
            "question": "Which of these sports is played with a ball?",
            "answers": ["A. Football", "B. Basketball", "C. Baseball", "D. Swimming"],
            "correct_answer": "D. Swimming"
        },
        {
            "question": "Which of these bird species does not fly?",
            "answers": ["A. Crow", "B. Penguins", "C. Ostriches", "D. Kiwi"],
            "correct_answer": "A. Crow"
        },
        {
            "question": "Which city is the capital of France?",
            "answers": ["A. Marcel", "B. Strasburg", "C. London", "D. Liyon"],
            "correct_answer": "C. London"
        },
        {
            "question": "Which of these is the ocean?",
            "answers": ["A. Pacific", "B. Atlantic", "C. Caribbean", "D. Indian"],
            "correct_answer": "C. Caribbean"
        }
    ]
    
    # Randomly select 5 questions
    selected_questions = random.sample(questions, NUM_QUESTIONS)
    
    # Create the display
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    # Load the background image and resize it to fit the window
    bg_image = pygame.image.load(BG_IMAGE_PATH)
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    
    # Initialize fonts
    question_font = pygame.font.Font(None, QUESTION_FONT_SIZE)
    answer_font = pygame.font.Font(None, ANSWER_FONT_SIZE)
    score_font = pygame.font.Font(None, 28)
    
    # Initialize game variables
    current_question_index = 0
    start_time = pygame.time.get_ticks() // 1000
    score = 0  # Initialize score
    
    # Create buttons list
    buttons = []
    
    # Function to create answer buttons
    def create_buttons(rect_x, rect_y):
        buttons.clear()
        question_data = selected_questions[current_question_index]
        answers = question_data["answers"]
        for i, answer in enumerate(answers):
            # Calculate button position
            button_x = rect_x + (RECT_WIDTH - BUTTON_WIDTH) // 2
            button_y = rect_y + 100 + (BUTTON_HEIGHT + BUTTON_MARGIN) * i
            
            # Create button rect
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            buttons.append((button_rect, answer))
    
    # Create buttons for the first question
    create_buttons((WIDTH - RECT_WIDTH) // 2 + 120, (HEIGHT - RECT_HEIGHT) // 2 - 60)
    
    timer = 0
    TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER, 250)
    cutscene = True
    # Create the main loop
    running = True
    while running:
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

            if timer != 20:
                window.blit(animation[timer % 20], (0, 0))
                window.blit(skip, (900, 600))
            else:
                cutscene = False

            # Draw the dark overlay on top
            something = 'This is cutscene'
            something_surface = question_font.render(something, True, 'white')
            window.blit(something_surface, (WIDTH // 2, HEIGHT // 2))
            window.blit(skip, (900, 600))
            pygame.display.update()
        
        else:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Toggle full window with F11
                    if event.key == pygame.K_F11:
                        if pygame.display.get_surface().get_flags() & pygame.FULLwindow:
                            pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        else:
                            pygame.display.set_mode((0, 0), pygame.FULLwindow)
                elif event.type == pygame.VIDEORESIZE:
                    # Resize the window
                    current_width, current_height = event.w, event.h
                    window = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                    # Resize the background image
                    bg_image = pygame.transform.scale(bg_image, (current_width, current_height))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    for button_rect, answer in buttons:
                        if button_rect.collidepoint(mouse_pos):
                            # If a button is clicked, check if the answer is correct
                            question_data = selected_questions[current_question_index]
                            if answer != question_data["correct_answer"]:
                                score += 1  # Increment score for incorrect answer

                            # Move to the next question if there is one
                            if current_question_index < NUM_QUESTIONS - 1:
                                current_question_index += 1
                                start_time = pygame.time.get_ticks() // 1000  # Reset the timer
                                create_buttons((WIDTH - RECT_WIDTH) // 2 + 120, (HEIGHT - RECT_HEIGHT) // 2 - 60)
                            else:
                                running = False  # End the game if there are no more questions

            # Calculate elapsed time and remaining time
            current_time = pygame.time.get_ticks() // 1000
            elapsed_time = current_time - start_time
            remaining_time = max(0, QUESTION_DURATION - elapsed_time)

            # Get current window size
            current_width, current_height = window.get_size()

            # Calculate rectangle position
            rect_x = (current_width - RECT_WIDTH) // 2 + 120  # Move right by 40 pixels
            rect_y = (current_height - RECT_HEIGHT) // 2 - 60  # Move up by 20 pixels

            # Draw the background image
            window.blit(bg_image, (0, 0))

            # Draw the rectangle outline
            pygame.draw.rect(window, (255, 255, 255), pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)

            # Draw the current question text at the top of the rectangle
            question_data = selected_questions[current_question_index]
            question_text = question_data["question"]
            question_surface = question_font.render(question_text, True, (255, 255, 255))
            question_x = rect_x + (RECT_WIDTH - question_surface.get_width()) // 2
            question_y = rect_y + 20  # Adjust the 20 offset as needed
            window.blit(question_surface, (question_x, question_y))

            # Draw the buttons with answers
            for button_rect, answer in buttons:
                pygame.draw.rect(window, (255, 255, 255), button_rect, 2)
                answer_surface = answer_font.render(answer, True, (255, 255, 255))
                answer_x = button_rect.x + (BUTTON_WIDTH - answer_surface.get_width()) // 2
                answer_y = button_rect.y + (BUTTON_HEIGHT - answer_surface.get_height()) // 2
                window.blit(answer_surface, (answer_x, answer_y))

            # Render the timer at the top center of the window
            timer_text = f"Time left: {remaining_time}s"
            timer_surface = question_font.render(timer_text, True, (255, 255, 255))
            timer_x = current_width // 2 - timer_surface.get_width() // 2
            timer_y = 20
            window.blit(timer_surface, (timer_x, timer_y))

            # Render the score at the top right of the window
            score_text = f"Score: {score}"
            score_surface = score_font.render(score_text, True, (255, 255, 255))
            score_x = current_width - score_surface.get_width() - 20
            score_y = 20
            window.blit(score_surface, (score_x, score_y))

            # Check if time is up for the current question
            if remaining_time <= 0:
                # Move to the next question if there is one
                if current_question_index < NUM_QUESTIONS - 1:
                    current_question_index += 1
                    start_time = current_time  # Reset the timer
                    create_buttons((WIDTH - RECT_WIDTH) // 2 + 120, (HEIGHT - RECT_HEIGHT) // 2 - 60)
                else:
                    running = False  # End the game if there are no more questions

            # Update the display
            pygame.display.flip()

    return
play((0, 0))
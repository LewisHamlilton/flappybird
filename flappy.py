import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 350
window_height = 622
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird with Skins")

# Create a clock object for controlling the frame rate
clock = pygame.time.Clock()

# Load obstacle images
obstacles = [
    pygame.image.load("bus2_1.png"),
    pygame.image.load("greenpipe.png")
]
selected_obs_index = 0

# Load skin images
skins = [
    pygame.image.load("angrybird.png"),
    pygame.image.load("ash.png"),
    pygame.image.load("blackbird.png"),
    pygame.image.load("piku.png"),
    pygame.image.load("star.png"),
    pygame.image.load("ufo.png"),
    pygame.image.load("img51.png")
]
selected_skin_index = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for button
font = pygame.font.Font(None, 36)

# Function to render the "Select" button
def render_select_button():
    button_text = font.render("Select", True, WHITE)
    button_rect = pygame.Rect(125, 500, 100, 50)
    pygame.draw.rect(screen, BLACK, button_rect)
    screen.blit(button_text, button_rect.topleft)
    return button_rect

# Function to render the "Back" button (after the game ends) at the top-left corner
def render_back_button():
    back_text = font.render("Back", True, WHITE)
    back_button_rect = pygame.Rect(10, 10, 100, 50)  # Positioning the button at top-left (10, 10)
    pygame.draw.rect(screen, BLACK, back_button_rect)
    screen.blit(back_text, back_button_rect.topleft)
    return back_button_rect

# Load background image
background = pygame.image.load("img54.png")  # Replace with your background image

# Function to handle the smooth skin transition (sliding effect)
def show_skin_transition(current_index, next_index, direction="right"):
    current_skin = skins[current_index]
    next_skin = skins[next_index]

    # Get dimensions of the skins
    current_width, current_height = current_skin.get_size()
    next_width, next_height = next_skin.get_size()

    # Initial positions of the skins
    current_skin_x = (window_width - current_width) / 2
    current_skin_y = (window_height - current_height) / 2
    next_skin_x = window_width if direction == "right" else -next_width
    next_skin_y = (window_height - next_height) / 2

    # Slide the skins horizontally (smooth transition)
    speed = 10
    for step in range(0, window_width, speed):
        screen.blit(background, (0, 0))  # Always draw the background first

        # Draw current skin moving out of the screen (center to left or center to right)
        screen.blit(current_skin, (current_skin_x - step if direction == "right" else current_skin_x + step, current_skin_y))

        # Draw next skin coming into the screen (from left or right to the center)
        screen.blit(next_skin, (next_skin_x - step + 140 if direction == "right" else next_skin_x + step - 140, next_skin_y))

        pygame.display.update()
        pygame.time.delay(10)  # Slow down the animation for smoothness

# Function for skin selection screen
def skin_selection():
    global selected_skin_index
    running = True
    while running:
        # Always fill with the background image first
        screen.blit(background, (0, 0))

        # Render the "Select" button
        select_button_rect = render_select_button()

        # Get dimensions of the current skin
        current_skin = skins[selected_skin_index]
        current_width, current_height = current_skin.get_size()

        # Calculate the center position of the current skin
        current_skin_x = (window_width - current_width) / 2
        current_skin_y = (window_height - current_height) / 2

        # Show current skin centered
        screen.blit(current_skin, (current_skin_x, current_skin_y))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button_rect.collidepoint(event.pos):
                    print(f"Skin {selected_skin_index + 1} selected.")
                    return True  # Proceed to obstacle selection after selecting the skin

            # Handle keypresses for navigating through skins
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Go to the previous skin (Right to Left transition)
                    next_index = (selected_skin_index - 1) % len(skins)
                    show_skin_transition(selected_skin_index, next_index, direction="left")
                    selected_skin_index = next_index
                elif event.key == pygame.K_RIGHT:  # Go to the next skin (Left to Right transition)
                    next_index = (selected_skin_index + 1) % len(skins)
                    show_skin_transition(selected_skin_index, next_index, direction="right")
                    selected_skin_index = next_index

        # Update the display
        pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)

# Function for obstacle selection screen
def obstacle_selection():
    global selected_obs_index
    running = True
    while running:
        # Always fill with the background image first
        screen.blit(background, (0, 0))

        # Render the "Select" button
        select_button_rect = render_select_button()

        # Get dimensions of the current obstacle
        current_obs = obstacles[selected_obs_index]
        current_width, current_height = current_obs.get_size()

        # Calculate the center position of the current obstacle
        current_obs_x = (window_width - current_width) / 2
        current_obs_y = (window_height - current_height) / 2

        # Show current obstacle centered
        screen.blit(current_obs, (current_obs_x, current_obs_y))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button_rect.collidepoint(event.pos):
                    print(f"Obstacle {selected_obs_index + 1} selected.")
                    return True  # Proceed to game loop after selecting the obstacle

            # Handle keypresses for navigating through obstacles
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Go to the previous obstacle (Right to Left transition)
                    next_index = (selected_obs_index - 1) % len(obstacles)
                    show_skin_transition(selected_obs_index, next_index, direction="left")
                    selected_obs_index = next_index
                elif event.key == pygame.K_RIGHT:  # Go to the next obstacle (Left to Right transition)
                    next_index = (selected_obs_index + 1) % len(obstacles)
                    show_skin_transition(selected_obs_index, next_index, direction="right")
                    selected_obs_index = next_index

        # Update the display
        pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)

# Function to update and display the score
def score_update():
    global score
    # Update the score
    for pipe in pipes:
        if pipe['rect'].right < bird_rect.left and not pipe.get('scored', False):
            score += 1
            pipe['scored'] = True  # Mark this pipe as scored

    # Render the score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (window_width - 150, 10))  # Positioning the score at the top-right

# Function to animate the pipes
def pipe_animation():
    global pipes
    for pipe in pipes:
        pipe['rect'].x -= 5  # Move the pipes to the left

        # If the pipe is out of the screen, remove it from the list
        if pipe['rect'].right < 0:
            pipes.remove(pipe)

        # Draw the pipes
        screen.blit(pipe['surface'], pipe['rect'])

# Function to generate new pipes
def create_pipes():
    height = random.randint(100, 400)
    gap = 200
    pipe_height = obstacles[selected_obs_index].get_height()

    top_pipe = obstacles[selected_obs_index]
    bottom_pipe = obstacles[selected_obs_index]
    
    top_rect = top_pipe.get_rect(midbottom=(window_width + 100, height - gap // 2))
    bottom_rect = bottom_pipe.get_rect(midtop=(window_width + 100, height + gap // 2))

    return [
        {'surface': top_pipe, 'rect': top_rect},
        {'surface': bottom_pipe, 'rect': bottom_rect}
    ]

# Function to draw floor (ground)
def draw_floor():
    global floor_x
    floor = pygame.image.load("img_50.png")  # Load your floor image here
    floor_width = floor.get_width()

    screen.blit(floor, (floor_x, window_height - floor.get_height()))
    screen.blit(floor, (floor_x + floor_width, window_height - floor.get_height()))

# Function to draw the score during the game or game over
def draw_score(state):
    if state == "game_on":
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (window_width - 150, 10))
    elif state == "game_over":
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 3))

# Game loop
def game_loop():
    global bird_rect, bird_movement, pipes, game_over, score, score_time, floor_x

    bird_img = skins[selected_skin_index]
    bird_rect = bird_img.get_rect(center=(67, window_height // 2))  # Use window_height instead of height
    bird_movement = 0
    gravity = 0.17

    pipes = []
    create_pipe = pygame.USEREVENT + 1
    pygame.time.set_timer(create_pipe, 1200)

    score = 0  # Initialize the score here
    game_over = False
    floor_x = 0  # Initialize floor_x for floor movement
    running = True

    while running:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    bird_movement = -7
                if event.button == 1 and game_over:
                    game_over = False
                    pipes = []
                    bird_movement = 0
                    bird_rect = bird_img.get_rect(center=(67, window_height // 2))  # Use window_height
                    score_time = True
                    score = 0  # Reset score on restart

            if event.type == create_pipe:
                pipes.extend(create_pipes())  # Add new pipes to the list

        screen.blit(background, (0, 0))  # Corrected this line to use background

        if not game_over:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

            if bird_rect.top < 5 or bird_rect.bottom >= 550:
                game_over = True

            screen.blit(rotated_bird, bird_rect)
            score_update()  # Call score update function here
            pipe_animation()  # Call pipe animation
            draw_score("game_on")  # Call draw_score function during the game
        else:
            draw_score("game_over")  # Display the game over screen

            # Render the "Back" button after the game is over
            back_button_rect = render_back_button()

            # Check for clicking the "Back" button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and back_button_rect.collidepoint(event.pos):
                        return  # Go back to skin selection

        floor_x -= 3
        if floor_x < -448:
            floor_x = 0

        draw_floor()  # Draw the moving floor
        pygame.display.update()


# Start the game after selections
def start_game():
    while True:
        if skin_selection():
            if obstacle_selection():
                game_loop()

# Start the game
start_game()

# Quit Pygame
pygame.quit()
sys.exit()

import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()

# Function to draw
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))


# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
    return top_pipe, bottom_pipe


# Function for animation
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True


# Function to draw score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
        screen.blit(high_score_text, high_score_rect)


# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score
        
# Set up the display window
window_width = 350
window_height = 622
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Flappy Birds")

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

# Load level images
levels = [
    pygame.image.load("greenpipelevel.png"),
    pygame.image.load("shootingstarlevel.png"),
    pygame.image.load("thunderlevel.png"),
    pygame.image.load("buslevel.png"),
    pygame.image.load("rocklevel.png")
]
selected_level_index = 0

# Load Background images
bckgs = [
    pygame.image.load("greenpipebkg.png"),
    pygame.image.load("shootingstarbckg.png"),
    pygame.image.load("thunderbckg.png"),
    pygame.image.load("busbckg.png"),
    pygame.image.load("rockbckg.png")
]
selected_bckg_index = 0

# Load Floor images
floors = [
    pygame.image.load("img_50.png"),
    pygame.image.load("shootingstarfloor.png"),
    pygame.image.load("lavafloor.png"),
    pygame.image.load("roadfloor.png"),
    pygame.image.load("waterfloor.png")
]
selected_floor_index = 0

# Load obstacle images
obstacles = [
    pygame.image.load("greenpipe.png"),
    pygame.image.load("shootingstar.png"),
    pygame.image.load("thunder1.png"),
    pygame.image.load("bus1.png"),
    pygame.image.load("rock.png")
]
selected_obs_index = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for button
font = pygame.font.Font(None, 36)

# Function to render the "Select" button
def render_select_button(text, x, y):
    button_text = font.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, 100, 50)
    pygame.draw.rect(screen, BLACK, button_rect)
    screen.blit(button_text, button_rect.topleft)
    return button_rect

# Load background image
background = pygame.image.load("img54.png")  # Replace with your background image

# Function to handle the smooth skin transition (sliding effect)
def show_transition(current_index, next_index, direction="right", items="skins"):
    current_item = skins[current_index] if items == "skins" else levels[current_index]
    next_item = skins[next_index] if items == "skins" else levels[next_index]

    # Get dimensions of the items
    current_width, current_height = current_item.get_size()
    next_width, next_height = next_item.get_size()

    # Initial positions of the items
    current_item_x = (window_width - current_width) / 2
    current_item_y = (window_height - current_height) / 2
    next_item_x = window_width if direction == "right" else -next_width
    next_item_y = (window_height - next_height) / 2

    # Slide the items horizontally (smooth transition)
    speed = 10
    for step in range(0, window_width, speed):
        screen.blit(background, (0, 0))  # Always draw the background first

        # Draw current item moving out of the screen (center to left or center to right)
        screen.blit(current_item, (current_item_x - step if direction == "right" else current_item_x + step, current_item_y))

        # Draw next item coming into the screen (from left or right to the center)
        screen.blit(next_item, (next_item_x - step + 140 if direction == "right" else next_item_x + step - 140, next_item_y))

        pygame.display.update()
        pygame.time.delay(10)  # Slow down the animation for smoothness

# Page 1 - Skin selection
def skin_selection_page():
    global selected_skin_index
    running = True
    while running:
        # Always fill with the background image first
        screen.blit(background, (0, 0))

        # Render the "Select" button
        select_button_rect = render_select_button("Select", 125, 500)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button_rect.collidepoint(event.pos):
                    print(f"Skin {selected_skin_index + 1} selected.")
                    return "level_selection"  # Proceed to the level selection page

            # Handle keypresses for navigating through skins
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Go to the previous skin (Right to Left transition)
                    next_index = (selected_skin_index - 1) % len(skins)
                    show_transition(selected_skin_index, next_index, direction="left", items="skins")
                    selected_skin_index = next_index
                elif event.key == pygame.K_RIGHT:  # Go to the next skin (Left to Right transition)
                    next_index = (selected_skin_index + 1) % len(skins)
                    show_transition(selected_skin_index, next_index, direction="right", items="skins")
                    selected_skin_index = next_index

        # Update the display
        pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)

# Page 2 - Level selection
def level_selection_page():
    global selected_level_index
    running = True
    while running:
        # Always fill with the background image first
        screen.blit(background, (0, 0))

        # Render the "Select" button
        select_button_rect = render_select_button("Select", 125, 500)

        # Get dimensions of the current level
        current_level = levels[selected_level_index]
        current_width, current_height = current_level.get_size()

        # Calculate the center position of the current level
        current_level_x = (window_width - current_width) / 2
        current_level_y = (window_height - current_height) / 2

        # Show current level centered
        screen.blit(current_level, (current_level_x, current_level_y))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button_rect.collidepoint(event.pos):
                    print(f"Level {selected_level_index + 1} selected.")
                    return selected_skin_index, selected_level_index  # Proceed to the final page with both selections

            # Handle keypresses for navigating through levels
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Go to the previous level (Right to Left transition)
                    next_index = (selected_level_index - 1) % len(levels)
                    show_transition(selected_level_index, next_index, direction="left", items="levels")
                    selected_level_index = next_index
                elif event.key == pygame.K_RIGHT:  # Go to the next level (Left to Right transition)
                    next_index = (selected_level_index + 1) % len(levels)
                    show_transition(selected_level_index, next_index, direction="right", items="levels")
                    selected_level_index = next_index

        # Update the display
        pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)

# Page 3 - Show selected skin and level
def show_selected_skin_and_level_page(selected_skin_index, selected_level_index):
    running = True
    while running:
        # Always fill with the background image first
        selected_bckg_index = selected_level_index  # Get background index from the selected level
        background = bckgs[selected_bckg_index]  # Define background here

        # Fill the screen with the background
        screen.blit(background, (0, 0))

        # Render the "Exit" button
        select_button_rect = render_select_button("Start", 125, 500)

        # Show selected skin
        current_skin = skins[selected_skin_index]
        current_width, current_height = current_skin.get_size()
        current_skin_x = (window_width - current_width) / 2
        current_skin_y = (window_height - 200 - current_height) / 3
        screen.blit(current_skin, (current_skin_x, current_skin_y))

        # Show selected level
        current_level = levels[selected_level_index]
        current_width, current_height = current_level.get_size()
        current_level_x = (window_width - current_width) / 2
        current_level_y = (window_height - current_height) / 1.5
        screen.blit(current_level, (current_level_x, current_level_y))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # If the window close button is clicked, exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if select_button_rect.collidepoint(event.pos):
                    #running = False  # If the "Exit" button is clicked, exit the program
                    print(f"Start the game with selected options.")
                    return selected_skin_index, selected_level_index  # Proceed to the final page with both selections
                    
        # Update the display
        pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)
        
# Page 4 - Main Game loop
def game_loop(selected_skin_index, selected_level_index):
    global pipes  # Declare pipes as a global variable
    running = True
    while running:
        # Always fill with the background image first
        selected_bckg_index = selected_level_index   # Get background index from the selected level
        selected_floor_index = selected_level_index
        selected_obs_index = selected_level_index
        background = bckgs[selected_bckg_index]  # Define background here
        back_img = bckgs[selected_bckg_index]
        floor_img = floors[selected_floor_index]
        floor_x = 0
        clock = pygame.time.Clock()

        # Fill the screen with the background
        screen.blit(background, (0, 0))

        # different stages of bird
        bird_up = skins[selected_skin_index]
        bird_down = skins[selected_skin_index]
        bird_mid = skins[selected_skin_index]
        birds = [bird_up, bird_mid, bird_down]
        bird_index = 0
        bird_flap = pygame.USEREVENT
        pygame.time.set_timer(bird_flap, 200)
        bird_img = birds[bird_index]
        bird_rect = bird_img.get_rect(center=(67, 622 // 2))
        bird_movement = 0
        gravity = 0.17

        # Loading pipe image
        pipe_img = obstacles[selected_obs_index]
        pipe_height = [400, 350, 533, 490]

        # for the pipes to appear
        pipes = []  # Initialize pipes here
        create_pipe = pygame.USEREVENT + 1
        pygame.time.set_timer(create_pipe, 1200)

        # Displaying game over image
        game_over = False
        over_img = pygame.image.load("img_45.png").convert_alpha()
        over_rect = over_img.get_rect(center=(window_width // 2, window_height // 2))

        # setting variables and font for score
        score = 0
        high_score = 0
        score_time = True
        score_font = pygame.font.Font("freesansbold.ttf", 27)

        # Game loop
        running = True
        while running:
            clock.tick(120)

            # for checking the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # QUIT event
                    running = False
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:  # Key pressed event
                    if event.button == 1 and not game_over:  # If space key is pressed
                        bird_movement = 0
                        bird_movement = -7

                    if event.button == 1 and game_over:
                        game_over = False
                        pipes = []  # Reset pipes when starting a new game
                        bird_movement = 0
                        bird_rect = bird_img.get_rect(center=(67, 622 // 2))
                        score_time = True
                        score = 0

                # To load different stages
                if event.type == bird_flap:
                    bird_index += 1

                    if bird_index > 2:
                        bird_index = 0

                    bird_img = birds[bird_index]
                    bird_rect = bird_up.get_rect(center=bird_rect.center)

                # To add pipes in the list
                if event.type == create_pipe:
                    pipes.extend(create_pipes())

            screen.blit(floor_img, (floor_x, 550))
            screen.blit(back_img, (0, 0))

            # Game over conditions
            if not game_over:
                bird_movement += gravity
                bird_rect.centery += bird_movement
                rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

                if bird_rect.top < 5 or bird_rect.bottom >= 550:
                    game_over = True

                screen.blit(rotated_bird, bird_rect)
                pipe_animation()  # Now the pipes variable is global and should work fine
                score_update()
                draw_score("game_on")
            elif game_over:
                screen.blit(over_img, over_rect)
                draw_score("game_over")

            # To move the base
            floor_x -= 3
            if floor_x < -448:
                floor_x = 0

            draw_floor()

            # Update the display
            pygame.display.update()

        # Delay for a short time before the next frame
        pygame.time.delay(100)

    # After exiting the loop, quit pygame and close the window
    pygame.quit()
    sys.exit()




# Main loop
def main():
    selected_skin_index = 0
    selected_level_index = 0
    page = "skin_selection"
    while True:
        if page == "skin_selection":
            page = skin_selection_page()  # Go to the skin selection page
        elif page == "level_selection":
            selected_skin_index, selected_level_index = level_selection_page()  # Go to the level selection page
            page = "show_selected"  # After level selection, show the selected skin and level page
        elif page == "show_selected":
            show_selected_skin_and_level_page(selected_skin_index, selected_level_index)  # Show selected skin and level
            page = "start_game"
        elif page == "start_game":
            game_loop(selected_skin_index, selected_level_index)

# Run the main loop
main()

# Quit Pygame
pygame.quit() 

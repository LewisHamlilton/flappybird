import pygame
import sys
import time
import random

# Initializing the pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()

# Game window
width, height = 350, 622
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird with Skins")



# Loading skin images (the same skins as on the skin selection page)
skins = [
    pygame.image.load("angrybird.png"),
    pygame.image.load("ash.png"),
    pygame.image.load("blackbird.png"),
    pygame.image.load("piku.png"),
    pygame.image.load("star.png"),
    pygame.image.load("ufo.png"),
    pygame.image.load("img51.png")
]
selected_skin_index = 0  # Set this value to the index of the selected skin from Page 1

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

#def read_and_display_selections():
try:
    # Open the file and read the selections
    with open("selections.txt", "r") as file:
        lines = file.readlines()
        selected_bckg_index = int(lines[0].split(":")[1].strip())
        selected_floor_index = int(lines[1].split(":")[1].strip())
        selected_obs_index = int(lines[2].split(":")[1].strip())
        selected_level_index = int(lines[3].split(":")[1].strip())
        selected_skin_index = int(lines[4].split(":")[1].strip())
        
        # Display the values
        print(f"Selected Background Index: {selected_bckg_index}")
        print(f"Selected Floor Index: {selected_floor_index}")
        print(f"Selected Obstacle Index: {selected_obs_index}")
        print(f"Selected Level Index: {selected_level_index}")
        print(f"Selected Skin Index: {selected_skin_index}")
except FileNotFoundError:
    print("Error: selections.txt file not found.")
except Exception as e:
    print(f"Error reading selections: {e}")

# Call the function to read and display the selections
#read_and_display_selections()

# Setting background and base image
back_img = bckgs[selected_bckg_index]#pygame.image.load("img54.png")
floor_img = floors[selected_floor_index]#pygame.image.load("img55.png")
floor_x = 0

# Loading pipe image
pipe_img = obstacles[selected_obs_index]#pygame.image.load("greenpipe.png")
pipe_height = [400, 350, 533, 490]

# Displaying game over image
over_img = pygame.image.load("img_45.png").convert_alpha()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# Setting variables and font for score
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 20)

# Function to draw the floor
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))

# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
    return top_pipe, bottom_pipe

# Function for pipe animation
def pipe_animation():
    global game_over
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

# Function to draw the score
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

# Game loop
def game_loop():
    global bird_rect, bird_movement, pipes, game_over, score, score_time, floor_x

    bird_img = skins[selected_skin_index]
    bird_rect = bird_img.get_rect(center=(67, height // 2))
    bird_movement = 0
    gravity = 0.17

    pipes = []
    create_pipe = pygame.USEREVENT + 1
    pygame.time.set_timer(create_pipe, 1200)

    game_over = False
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
                    bird_rect = bird_img.get_rect(center=(67, height // 2))
                    score_time = True
                    score = 0

            if event.type == create_pipe:
                pipes.extend(create_pipes())

        screen.blit(back_img, (0, 0))

        if not game_over:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

            if bird_rect.top < 5 or bird_rect.bottom >= 550:
                game_over = True

            screen.blit(rotated_bird, bird_rect)
            pipe_animation()
            score_update()
            draw_score("game_on")
        else:
            screen.blit(over_img, over_rect)
            draw_score("game_over")

        floor_x -= 3
        if floor_x < -448:
            floor_x = 0

        draw_floor()
        pygame.display.update()

# Main Execution
game_loop()

# Quitting the game
pygame.quit()
sys.exit()

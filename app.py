import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display window
window_width = 350
window_height = 622
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Skin Selector")

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

# Main loop
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select_button_rect.collidepoint(event.pos):
                print(f"Skin {selected_skin_index + 1} selected.")
        
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

# Quit Pygame
pygame.quit()
sys.exit()

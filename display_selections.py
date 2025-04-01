import pygame
# Initialize Pygame
pygame.init()
import sys

# Check if username is provided
if len(sys.argv) > 1:
    username = sys.argv[1]
    print(username)
else:
    username = "Player"  # Default name if no username is passed
import pymysql    
import subprocess

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

def open_level(selected_skin_index, selected_level_index, username):
    subprocess.run(["python", "level.py", username, str(selected_skin_index), str(selected_level_index)])

# Load background image
background = pygame.image.load("tree.png")  # Replace with your background image

score_font = pygame.font.Font("freesansbold.ttf", 20)  # Define the font
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

def get_high_score(username):
    try:
        con = pymysql.connect(host='localhost', user='root', password='aditya', database='userdatu')
        cursor = con.cursor()

        cursor.execute("SELECT high_score FROM data WHERE username=%s", (username,))
        result = cursor.fetchone()

        con.close()

        if result:
            return result[0]
        return 0
    except Exception as e:
        print("Database error:", e)
        return 0

print("Your High Score:", get_high_score(username))

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
        # Display welcome message
        welcome_text = score_font.render(f"Welcome, {username}!", True, (255, 255, 255))
        screen.blit(welcome_text, (20, 20))  # Position at top-left
        # Render the "Select" button
        select_button_rect = render_select_button("Select", 125, 500)
        # Show the current skin
        current_skin = skins[selected_skin_index]
        screen.blit(current_skin, ((window_width - current_skin.get_width()) / 2, (window_height - current_skin.get_height()) / 2))
        

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
    global selected_bckg_index, selected_floor_index, selected_obs_index
    running = True
    while running:
        # Set all indices to selected_level_index
        selected_bckg_index = selected_level_index
        selected_floor_index = selected_level_index
        selected_obs_index = selected_level_index

        # Always fill with the background image first
        #background = bckgs[selected_bckg_index]

        # Fill the screen with the background
        screen.blit(background, (0, 0))

        # Render the "Start Game" button
        start_button_rect = render_select_button("Start", 125, 500)

        # Show selected skin
        current_skin = skins[selected_skin_index]
        screen.blit(current_skin, ((window_width - current_skin.get_width()) / 2, (window_height - 200 - current_skin.get_height()) / 3))

        # Show selected level
        current_level = levels[selected_level_index]
        screen.blit(current_level, ((window_width - current_level.get_width()) / 2, (window_height - current_level.get_height()) / 1.5))

        # Save selections to a file
        with open("selections.txt", "w") as file:
            file.write(f"Selected Background Index: {selected_bckg_index}\n")
            file.write(f"Selected Floor Index: {selected_floor_index}\n")
            file.write(f"Selected Obstacle Index: {selected_obs_index}\n")
            file.write(f"Selected Level Index: {selected_level_index}\n")
            file.write(f"Selected Skin Index: {selected_skin_index}\n")

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit if window is closed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    pygame.quit()  # Close current Pygame window
                    subprocess.run(["python", "level.py", username, str(selected_skin_index), str(selected_level_index)])

        # Update the display
        pygame.display.update()
        pygame.time.delay(100)

    # Quit pygame after exiting the loop
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

# Run the main loop
main()

# Quit Pygame
pygame.quit() 

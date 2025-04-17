import pygame
import random
import os
import json  # To handle saving progress in JSON

# Initialize Pygame
pygame.init()

# Game variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 5
is_jumping = False
jump_count = 10

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacles = []

# Game loop
def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles  # Ensure global scope for variables

    clock = pygame.time.Clock()
    run_game = True
    start_ticks = pygame.time.get_ticks()  # Track the start time

    while run_game:
        screen.fill(WHITE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT]:
            player_x += player_velocity
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Collision and obstacle logic
        for obs in obstacles:
            if obs.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                print("Game Over!")
                run_game = False

        # Create obstacles
        if random.random() < 0.01:
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacles.append(pygame.Rect(obstacle_x, -obstacle_height, obstacle_width, obstacle_height))

        # Move obstacles
        for obs in obstacles:
            obs.y += 5
            pygame.draw.rect(screen, RED, obs)
            if obs.y > screen_height:
                obstacles.remove(obs)

        # Draw player
        pygame.draw.rect(screen, BLACK, pygame.Rect(player_x, player_y, player_width, player_height))

        # Check if the player has survived for 10 seconds
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 10000:  # 10 seconds (10000 milliseconds)
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before closing
            run_game = False

            # Update level in pass.json after winning
            update_level_progress(level)

            # After win, run lmenu.py
            os.system('python lmenu.py')  # Runs the lmenu.py script

        # Update display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def update_level_progress(level):
    # File to store progress
    progress_file = 'pass.json'

    # Check if the file exists
    if os.path.exists(progress_file):
        # Load the current progress
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    else:
        # Initialize an empty progress dictionary if file doesn't exist
        progress = {}

    # Update the level passed to True
    level_key = f"level_{level}"
    if level_key in progress:
        progress[level_key] = True
    else:
        progress[level_key] = True  # In case the level does not exist in the progress

    # Save the progress back to the file
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=4)

# Run the game for level 1
game_loop(1)

import pygame
import random
import os
import json

pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner - Level 5")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY  = (150, 150, 150)

# Player setup (even smaller)
player_width = 30
player_height = 30
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 8
is_jumping = False
jump_count = 10

# Obstacle structure: list of dicts with Rect, dx, dy, is_fake
obstacles = []

def random_color():
    return (random.randint(50,255), random.randint(50,255), random.randint(50,255))

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles

    clock = pygame.time.Clock()
    run_game = True
    start_ticks = pygame.time.get_ticks()

    # Designate 1 fake obstacle index to change color
    color_changer_index = None

    while run_game:
        screen.fill(WHITE)

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
                neg = 1 if jump_count > 0 else -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Spawn obstacles
        if len(obstacles) < 12 and random.random() < 0.25:
            obs_x = random.randint(0, screen_width - 40)
            dx = random.choice([-3, -2, -1, 1, 2, 3])
            is_fake = random.random() < 0.2  # 20% chance it's fake
            obstacles.append({
                "rect": pygame.Rect(obs_x, -40, 40, 40),
                "dx": dx,
                "dy": 12,
                "is_fake": is_fake,
                "color": GRAY if is_fake else RED
            })
            if is_fake and color_changer_index is None:
                color_changer_index = len(obstacles) - 1

        # Update obstacles
        for i, obs in enumerate(obstacles):
            obs["rect"].y += obs["dy"]
            obs["rect"].x += obs["dx"]

            # Bounce from wall
            if obs["rect"].left <= 0 or obs["rect"].right >= screen_width:
                obs["dx"] *= -1

            # Color changer
            if i == color_changer_index:
                obs["color"] = random_color()

            pygame.draw.rect(screen, obs["color"], obs["rect"])

        # Clean up off-screen
        obstacles = [obs for obs in obstacles if obs["rect"].y < screen_height]

        # Collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obs in obstacles:
            if not obs["is_fake"] and player_rect.colliderect(obs["rect"]):
                print("Game Over!")
                run_game = False

        # Draw player
        pygame.draw.rect(screen, BLACK, player_rect)

        # Win condition
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 10000:
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            update_level_progress(level)
            os.system('python lmenu.py')
            run_game = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def update_level_progress(level):
    progress_file = 'pass.json'
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    else:
        progress = {}

    level_key = f"level_{level}"
    progress[level_key] = True

    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=4)

# Run Level 5
game_loop(5)

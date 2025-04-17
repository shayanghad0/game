import pygame
import random
import os
import json

# Initialize Pygame
pygame.init()

# Game settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner - Level 3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings (slightly smaller to make it trickier)
player_width = 40
player_height = 40
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 6
is_jumping = False
jump_count = 10

# Obstacle list
obstacles = []

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles

    clock = pygame.time.Clock()
    run_game = True
    start_ticks = pygame.time.get_ticks()

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
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Spawn more aggressive obstacles
        if len(obstacles) < 7 and random.random() < 0.15:
            obstacle_x = random.randint(0, screen_width - 50)
            obstacles.append(pygame.Rect(obstacle_x, -50, 50, 50))

        # Move & draw obstacles
        for obs in obstacles:
            obs.y += 8  # Faster than level 2
            pygame.draw.rect(screen, RED, obs)

        # Remove off-screen
        obstacles = [obs for obs in obstacles if obs.y < screen_height]

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obs in obstacles:
            if player_rect.colliderect(obs):
                print("Game Over!")
                run_game = False

        # Draw player
        pygame.draw.rect(screen, BLACK, player_rect)

        # Win after 10 seconds
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

# Start Level 3
game_loop(3)

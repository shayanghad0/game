import pygame
import random
import os
import json
import math

pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner - Level 8")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GRAY  = (150, 150, 150)

# Player
player_width = 30
player_height = 30
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 8
is_jumping = False
jump_count = 10
gravity_flipped = False

# Obstacles, enemies, lasers
obstacles = []
chasers = []
lasers = []

# Timers
gravity_timer = 0
gravity_interval = 5000
laser_timer = 0
laser_interval = 2000

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles, gravity_flipped
    global gravity_timer, laser_timer, chasers, lasers

    clock = pygame.time.Clock()
    run_game = True
    start_ticks = pygame.time.get_ticks()

    while run_game:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        now = pygame.time.get_ticks()

        # Gravity flip
        if now - gravity_timer > gravity_interval:
            gravity_flipped = not gravity_flipped
            gravity_timer = now

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
                if gravity_flipped:
                    player_y += (jump_count ** 2) * 0.4 * neg
                else:
                    player_y -= (jump_count ** 2) * 0.4 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Boundaries
        player_x = max(0, min(player_x, screen_width - player_width))
        player_y = max(0, min(player_y, screen_height - player_height))
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Spawn falling obstacles
        if len(obstacles) < 18 and random.random() < 0.4:
            obs_x = random.randint(0, screen_width - 40)
            dy = 18 if not gravity_flipped else -18
            y_pos = -40 if not gravity_flipped else screen_height + 40
            obstacles.append(pygame.Rect(obs_x, y_pos, 40, 40))

        # Move obstacles
        for obs in obstacles:
            obs.y += dy
            pygame.draw.rect(screen, RED, obs)

        # Remove off-screen
        obstacles = [obs for obs in obstacles if 0 <= obs.y <= screen_height]

        # Spawn chasers
        if len(chasers) < 2:
            chaser_x = random.choice([0, screen_width - 30])
            chaser_y = random.randint(0, screen_height - 30)
            chasers.append(pygame.Rect(chaser_x, chaser_y, 30, 30))

        # Move chasers toward player
        for chaser in chasers:
            dx = player_x - chaser.x
            dy = player_y - chaser.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                chaser.x += int(3 * dx / dist)
                chaser.y += int(3 * dy / dist)
            pygame.draw.rect(screen, BLUE, chaser)

        # Laser logic (spawn and blink)
        if now - laser_timer > laser_interval:
            laser_timer = now
            if not lasers:
                # Horizontal laser
                lasers.append(("h", pygame.Rect(0, random.randint(100, 500), screen_width, 5)))
                # Vertical laser
                lasers.append(("v", pygame.Rect(random.randint(100, 700), 0, 5, screen_height)))
            else:
                lasers.clear()

        for direction, laser in lasers:
            pygame.draw.rect(screen, GRAY, laser)

        # Draw player
        pygame.draw.rect(screen, BLACK, player_rect)

        # Collisions
        for obs in obstacles:
            if player_rect.colliderect(obs):
                print("Game Over - Obstacle!")
                run_game = False
        for chaser in chasers:
            if player_rect.colliderect(chaser):
                print("Game Over - Chased!")
                run_game = False
        for _, laser in lasers:
            if player_rect.colliderect(laser):
                print("Game Over - Zapped!")
                run_game = False

        # Win after 25 seconds
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 25000:
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2,
                               screen_height // 2 - text.get_height() // 2))
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

# Run Level 8
game_loop(8)

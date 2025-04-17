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
pygame.display.set_caption("Rage Runner - Level 9")

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
teleport_timer = 0

# Obstacles, enemies, lasers, platforms
obstacles = []
chasers = []
lasers = []
platforms = []

# Timers
gravity_timer = 0
gravity_interval = 5000
teleport_interval = 3000

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles, gravity_flipped
    global gravity_timer, teleport_timer, chasers, lasers, platforms

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

        # Teleporting Player every 3 seconds
        if now - teleport_timer > teleport_interval:
            player_x = random.randint(0, screen_width - player_width)
            player_y = random.randint(0, screen_height - player_height)
            teleport_timer = now

        # Split controls: Arrow Keys + WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_velocity
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_velocity

        # Boundaries
        player_x = max(0, min(player_x, screen_width - player_width))
        player_y = max(0, min(player_y, screen_height - player_height))
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Spawn falling obstacles
        if len(obstacles) < 20 and random.random() < 0.5:
            obs_x = random.randint(0, screen_width - 40)
            dy = 20 if not gravity_flipped else -20
            y_pos = -40 if not gravity_flipped else screen_height + 40
            obstacles.append(pygame.Rect(obs_x, y_pos, 40, 40))

        # Move obstacles
        for obs in obstacles:
            obs.y += dy
            pygame.draw.rect(screen, RED, obs)

        # Remove off-screen
        obstacles = [obs for obs in obstacles if 0 <= obs.y <= screen_height]

        # Spawn chasers
        if len(chasers) < 3:
            chaser_x = random.choice([0, screen_width - 30])
            chaser_y = random.randint(0, screen_height - 30)
            chasers.append(pygame.Rect(chaser_x, chaser_y, 30, 30))

        # Move chasers toward player
        for chaser in chasers:
            dx = player_x - chaser.x
            dy = player_y - chaser.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                chaser.x += int(4 * dx / dist)
                chaser.y += int(4 * dy / dist)
            pygame.draw.rect(screen, BLUE, chaser)

        # Platform shifting: create platforms that move up and down
        if random.random() < 0.1:
            plat_x = random.randint(0, screen_width - 60)
            plat_y = random.randint(100, screen_height - 50)
            platforms.append(pygame.Rect(plat_x, plat_y, 60, 10))

        for plat in platforms:
            plat.y += random.choice([-2, 2])
            pygame.draw.rect(screen, GRAY, plat)

        # Collision with obstacles
        for obs in obstacles:
            if player_rect.colliderect(obs):
                print("Game Over - Obstacle!")
                run_game = False

        # Collision with chasers
        for chaser in chasers:
            if player_rect.colliderect(chaser):
                print("Game Over - Chased!")
                run_game = False

        # Collision with platforms (player must stand on them)
        for plat in platforms:
            if player_rect.colliderect(plat):
                player_y = plat.y - player_height  # Snap player to platform

        # Draw player
        pygame.draw.rect(screen, BLACK, player_rect)

        # Win after 30 seconds
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 30000:
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

# Run Level 9
game_loop(9)

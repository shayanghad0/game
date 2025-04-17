import pygame
import random
import os
import json
import math

pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner - Boss Fight")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GRAY  = (150, 150, 150)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Player
player_width = 30
player_height = 30
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 8
is_jumping = False
jump_count = 10
gravity_flipped = False

# Boss setup
boss_width = 150
boss_height = 150
boss_x = screen_width // 2 - boss_width // 2
boss_y = screen_height // 3
boss_health = 100

# Obstacles, enemies, lasers
obstacles = []
chasers = []
lasers = []
platforms = []
projectiles = []

# Timers
gravity_timer = 0
gravity_interval = 5000
teleport_timer = 0
laser_timer = 0

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles, gravity_flipped
    global gravity_timer, teleport_timer, chasers, lasers, platforms, projectiles, boss_health, boss_x, boss_y

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
        if now - teleport_timer > 3000:
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

        # Boss Movement: The boss moves to attack the player
        if boss_health > 0:
            # Boss randomly summons obstacles
            if random.random() < 0.1:
                obs_x = random.randint(0, screen_width - 40)
                obs_y = random.randint(0, screen_height - 40)
                obstacles.append(pygame.Rect(obs_x, obs_y, 40, 40))
            
            # Boss lasers (shoots toward the player)
            if random.random() < 0.1:
                laser_x = boss_x + boss_width // 2
                laser_y = boss_y + boss_height
                lasers.append(pygame.Rect(laser_x, laser_y, 5, 50))

            pygame.draw.rect(screen, PURPLE, (boss_x, boss_y, boss_width, boss_height))

        # Draw obstacles
        for obs in obstacles:
            obs.y += 10
            pygame.draw.rect(screen, RED, obs)

        obstacles = [obs for obs in obstacles if 0 <= obs.y <= screen_height]

        # Draw lasers
        for laser in lasers:
            laser.y += 10
            pygame.draw.rect(screen, YELLOW, laser)

        lasers = [laser for laser in lasers if laser.y <= screen_height]

        # Chasers (faster than before)
        for chaser in chasers:
            dx = player_x - chaser.x
            dy = player_y - chaser.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                chaser.x += int(5 * dx / dist)
                chaser.y += int(5 * dy / dist)
            pygame.draw.rect(screen, BLUE, chaser)

        # Spawn projectiles (boss attacks)
        if random.random() < 0.05:
            projectile_x = boss_x + boss_width // 2
            projectile_y = boss_y + boss_height
            projectiles.append(pygame.Rect(projectile_x, projectile_y, 10, 10))

        for proj in projectiles:
            proj.y += 5
            pygame.draw.rect(screen, RED, proj)

        projectiles = [proj for proj in projectiles if proj.y <= screen_height]

        # Collision checks
        for obs in obstacles:
            if player_rect.colliderect(obs):
                print("Game Over - Hit an obstacle!")
                run_game = False

        for laser in lasers:
            if player_rect.colliderect(laser):
                print("Game Over - Laser hit!")
                run_game = False

        for chaser in chasers:
            if player_rect.colliderect(chaser):
                print("Game Over - Chased!")
                run_game = False

        for proj in projectiles:
            if player_rect.colliderect(proj):
                print("Game Over - Hit by projectile!")
                run_game = False

        # Boss collision with player
        if pygame.Rect(boss_x, boss_y, boss_width, boss_height).colliderect(player_rect):
            boss_health -= 1

        # Win condition (after 40 seconds)
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 40000:
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WIN!", True, GREEN)
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

# Run Boss Fight Level
game_loop(10)

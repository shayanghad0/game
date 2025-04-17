import pygame
import random
import os
import json

pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rage Runner - Level 7")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY  = (120, 120, 120)

# Player
player_width = 30
player_height = 30
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_velocity = 8
is_jumping = False
jump_count = 10
gravity_flipped = False

# Obstacles
obstacles = []

# Gravity flip
gravity_timer = 0
gravity_interval = 5000  # flip gravity every 5 sec

def game_loop(level):
    global player_x, player_y, is_jumping, jump_count, obstacles, gravity_flipped, gravity_timer

    clock = pygame.time.Clock()
    run_game = True
    start_ticks = pygame.time.get_ticks()

    while run_game:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Gravity flip logic
        now = pygame.time.get_ticks()
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

        # Keep player in bounds
        player_x = max(0, min(player_x, screen_width - player_width))
        player_y = max(0, min(player_y, screen_height - player_height))

        # Spawn obstacles
        if len(obstacles) < 16 and random.random() < 0.35:
            obs_x = random.randint(0, screen_width - 40)
            dx = random.choice([-4, -3, -2, 2, 3, 4])
            is_fake = random.random() < 0.1
            dy = 16 if not gravity_flipped else -16
            y_pos = -40 if not gravity_flipped else screen_height + 40
            obstacles.append({
                "rect": pygame.Rect(obs_x, y_pos, 40, 40),
                "dx": dx,
                "dy": dy,
                "is_fake": is_fake,
                "color": GRAY if is_fake else RED
            })

        # Update and draw obstacles
        for obs in obstacles:
            obs["rect"].y += obs["dy"]
            obs["rect"].x += obs["dx"]
            if obs["rect"].left <= 0 or obs["rect"].right >= screen_width:
                obs["dx"] *= -1
            pygame.draw.rect(screen, obs["color"], obs["rect"])

        # Remove off-screen
        if gravity_flipped:
            obstacles = [obs for obs in obstacles if obs["rect"].y > -50]
        else:
            obstacles = [obs for obs in obstacles if obs["rect"].y < screen_height + 50]

        # Collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obs in obstacles:
            if not obs["is_fake"] and player_rect.colliderect(obs["rect"]):
                print("Game Over!")
                run_game = False

        # Draw player
        pygame.draw.rect(screen, BLACK, player_rect)

        # Win condition — survive 20 seconds
        time_passed = pygame.time.get_ticks() - start_ticks
        if time_passed >= 20000:
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

# Run Level 7
game_loop(7)

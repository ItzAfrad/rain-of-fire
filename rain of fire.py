import pygame
import random
import sys
import os
import time

pygame.init()
pygame.mixer.init()

# Get the absolute path to the script or the bundled executable
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))
# Load high score from file or default to 0
high_score = 0
high_score_file_path = os.path.join(script_dir, "high_score.txt")

if os.path.exists(high_score_file_path):
    with open(high_score_file_path, 'r') as file:
        try:
            high_score = int(file.read())
        except ValueError:
            pass
game_over = False

# Setting up the display
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Rain of Fire")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

player = pygame.image.load(os.path.join(script_dir, "player.png")).convert_alpha()
enemy = pygame.image.load(os.path.join(script_dir, "enemy.png")).convert_alpha()
bg = pygame.image.load(os.path.join(script_dir, "bg.png"))
background_music_files = pygame.mixer.Sound(os.path.join(script_dir, "bg_music.mp3"))
pygame.display.set_icon(enemy)

# Load high score from file or default to 0
high_score = 0
high_score_file_path = os.path.join(script_dir, "high_score.txt")

if os.path.exists(high_score_file_path):
    with open(high_score_file_path, 'r') as file:
        try:
            high_score = int(file.read())
        except ValueError:
            pass

# Spawning the player
player_x = 450
player_y = 510
player_speed = 5

# Spawning enemies
enemies = []
num_enemies = 10
for _ in range(num_enemies):
    enemy_x = random.randrange(0, 900 - enemy.get_width())
    enemy_y = random.randrange(-100, -40)
    enemy_speed = random.randint(1, 3)
    enemies.append((enemy_x, enemy_y, enemy_speed))

# Load background music
pygame.mixer.music.load(os.path.join(script_dir, "bg_music.mp3"))
pygame.mixer.music.play(-1)  # Play the background music indefinitely

# Initialize game timer
start_time = time.time()
elapsed_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score to a file before quitting
            with open(high_score_file_path, 'w') as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()

    # Clear the screen (Set the background color to black)
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    # Player animation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    elif keys[pygame.K_LEFT]:
        player_x -= player_speed

    # Keep the player within the window bounds
    player_x = max(0, min(player_x, 900 - player.get_width()))

    # Draw the player and update player_hitbox
    screen.blit(player, (player_x, player_y))
    player_hitbox = player.get_rect().move(player_x, player_y)

    # Draw enemies and check for collisions
    for i, enemy_data in enumerate(enemies):
        enemy_x, enemy_y, enemy_speed = enemy_data[:3]
        enemy_hitbox = enemy.get_rect().move(enemy_x, enemy_y)
        screen.blit(enemy, (enemy_x, enemy_y))

        if player_hitbox.colliderect(enemy_hitbox):
            # If the player collides with an enemy, it's game over
            game_over = True
            font = pygame.font.Font(None, 70)
            text = font.render("GAME OVER! Press space to restart", True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)

        # Update the enemy position
        enemy_y += enemy_speed
        if enemy_y > 600:
            # If the enemy goes off the screen, respawn it above the window
            enemy_x = random.randrange(0, 900 - enemy.get_width())
            enemy_y = random.randrange(-100, -40)
            enemy_speed = random.randint(1, 3)
            enemies[i] = (enemy_x, enemy_y, enemy_speed)
        else:
            # Store the updated enemy data back into the list
            enemies[i] = (enemy_x, enemy_y, enemy_speed)

    # Update the elapsed time
    if not game_over:
        elapsed_time = time.time() - start_time

    # Check and update the high score
    if elapsed_time > high_score:
        high_score = elapsed_time

    # Display the elapsed time and high score on the screen
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {int(elapsed_time)} seconds", True, (0, 255, 0))
    screen.blit(timer_text, (10, 10))

    high_score_text = font.render(f"High Score: {int(high_score)} seconds", True, (0, 255, 0))
    screen.blit(high_score_text, (screen.get_width() - high_score_text.get_width() - 10, 10))

    if game_over:
        pygame.mixer.music.stop()#stop music and pause game
        # Save the high score to a file after the game over loop
        with open(high_score_file_path, 'w') as file:
            file.write(str(high_score))
            print("Saved high score:", high_score)
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save the high score to a file before quitting
                    with open(high_score_file_path, 'w') as file:
                        file.write(str(high_score))
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset the game and start a new game
                        pygame.mixer.music.play(-1)
                        game_over = False
                        player_x = 450
                        player_y = 510
                        start_time = time.time()
                        elapsed_time = 0  # Reset the timer
                        for i in range(num_enemies):
                            enemy_x = random.randrange(0, 900 - enemy.get_width())
                            enemy_y = random.randrange(-100, -40)
                            enemy_speed = random.randint(1, 3)
                            enemies[i] = (enemy_x, enemy_y, enemy_speed)
                        break

            pygame.display.update()
            clock.tick(60)
        # Save the high score to a file after the game over loop
        try:
            with open(high_score_file_path, 'w') as file:
                file.write(str(high_score))
                print("Saved high score:", high_score)
        except Exception as e:
            print("Error saving high score:", e)

    else:
        # Update the game if it's not game over
        pygame.display.update()
        clock.tick(60)

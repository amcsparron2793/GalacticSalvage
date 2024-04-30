#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources from abandoned space stations and derelict ships. Navigate through asteroid fields, avoid enemy patrols, and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galactic Salvage")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player properties
player_width = 50
player_height = 50
player_color = (0, 255, 0)
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 20
player_speed = 5

# Projectile properties
projectile_width = 5
projectile_height = 15  # Adjusted for consistent size
projectile_color = (255, 0, 0)

projectile_speed = 7
projectile_cooldown = 30  # Cooldown period in frames
cooldown_counter = 0

projectiles = []

# Game loop

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        break

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Check if cooldown is over and spacebar is pressed

    if keys[pygame.K_SPACE] and cooldown_counter <= 0:
        # Fire projectile
        projectile_x = player_x + player_width // 2 - projectile_width // 2
        projectile_y = player_y
        projectiles.append([projectile_x, projectile_y])

        cooldown_counter = projectile_cooldown  # Reset cooldown

    # Update cooldown counter
    if cooldown_counter > 0:
        cooldown_counter -= 1

    # Update projectiles
    for projectile in projectiles:
        projectile[1] -= projectile_speed

        pygame.draw.rect(screen, projectile_color, (projectile[0], projectile[1], projectile_width, projectile_height))

        # Remove projectiles that go off-screen
        if projectile[1] < 0:
            projectiles.remove(projectile)

    # Draw player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()

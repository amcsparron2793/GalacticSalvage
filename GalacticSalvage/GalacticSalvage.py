#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources from abandoned space stations and derelict ships. Navigate through asteroid fields, avoid enemy patrols, and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""
import pygame
from typing import Tuple


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


class Player:
    def __init__(self, color: Tuple[int, int, int] = (0, 255, 0), projectile_cooldown: int = 30):
        self.width = 50
        self.height = 50
        self.color = color
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 5
        self.projectile_cooldown = projectile_cooldown  # Cooldown period in frames
        self.cooldown_counter = 0

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed


class Projectile:
    def __init__(self, x, y):
        self.width = 5
        self.height = 15
        self.color = (255, 0, 0)
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed


def run_game():
    running = True
    clock = pygame.time.Clock()

    player = Player()
    projectiles = []

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            break

        if keys[pygame.K_LEFT]:
            player.move_left()

        if keys[pygame.K_RIGHT]:
            player.move_right()

        # Check if spacebar is pressed to shoot
        if keys[pygame.K_SPACE] and player.cooldown_counter <= 0:
            # Fire projectile
            projectile_x = player.x + player.width // 2 - 2  # Adjusted for projectile width
            projectile_y = player.y
            projectiles.append(Projectile(projectile_x, projectile_y))
            player.cooldown_counter = player.projectile_cooldown

        if player.cooldown_counter > 0:
            player.cooldown_counter -= 1

        # Update projectiles
        for projectile in projectiles:
            projectile.move()
            pygame.draw.rect(screen, projectile.color, (projectile.x, projectile.y, projectile.width, projectile.height))
            # Remove projectiles that go off-screen
            if projectile.y < 0:
                projectiles.remove(projectile)

        # Draw player
        pygame.draw.rect(screen, player.color, (player.x, player.y, player.width, player.height))

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    run_game()

#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources
from abandoned space stations and derelict ships.
Navigate through asteroid fields, avoid enemy patrols,
and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""
import pygame
from typing import Tuple, List
import random


# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Settings:
    # Set up the screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Galactic Salvage")


class Player:
    def __init__(self, color: Tuple[int, int, int] = (0, 255, 0), projectile_cooldown: int = 15):
        self.width = 50
        self.height = 50
        self.color = color
        self.x = Settings.SCREEN_WIDTH // 2 - self.width // 2
        self.y = Settings.SCREEN_HEIGHT - self.height - 20
        self.speed = 5
        self.projectile_cooldown = projectile_cooldown  # Cooldown period in frames
        self.cooldown_counter = 0
        self.blaster = pygame.mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.boom = pygame.mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')
        # TODO: add score var etc.

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < Settings.SCREEN_WIDTH - self.width:
            self.x += self.speed


class Projectile:
    def __init__(self, x, y, color: Tuple[int, int, int] = (255, 0, 0)):
        self.width = 5
        self.height = 15
        self.color = color
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed


class Asteroid:
    def __init__(self):
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        self.x = random.randint(0, Settings.SCREEN_WIDTH - self.width)
        self.y = -self.height  # Start above the screen
        self.speed = random.randint(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Random rotation speed
        self.boom = pygame.mixer.Sound('../Misc_Project_Files/sounds/BoomAsteroid.mp3')

    def move(self):
        self.y += self.speed
        self.angle += self.rotation_speed

    def draw(self, screen):
        # Create a surface for the asteroid and rotate it
        asteroid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(asteroid_surface, self.color, (0, 0, self.width, self.height))
        # pygame.draw.polygon(asteroid_surface, self.color, (polys), self.width)#, self.height))
        rotated_surface = pygame.transform.rotate(asteroid_surface, self.angle)
        # Get the rect of the rotated surface and set its center to the asteroid's position
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        # Draw the rotated surface onto the screen
        screen.blit(rotated_surface, rotated_rect)


def _UpdateBulletProjectiles(projectiles: List[Projectile]):
    # Update projectiles
    for projectile in projectiles:
        projectile.move()
        pygame.draw.rect(Settings.screen, projectile.color,
                         (projectile.x, projectile.y,
                          projectile.width, projectile.height))
        # Remove projectiles that go off-screen
        if projectile.y < 0:
            projectiles.remove(projectile)
    return projectiles


def _UpdateAsteroids(asteroids: List[Asteroid]):
    # Update asteroids
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw(Settings.screen)  # Draw the asteroid with rotation
        # Remove asteroids that go off-screen
        if asteroid.y > Settings.SCREEN_HEIGHT:
            asteroids.remove(asteroid)
    return asteroids


def _CheckCollisions(projectiles: List[Projectile], asteroids: List[Asteroid], player: Player):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for asteroid in asteroids:
        # create a hit box around the asteroid
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
        # if the two hit boxes collide, then remove the projectile and the asteroid
        if player_rect.colliderect(asteroid_rect):
            mx = player.boom.play()
            while mx.get_busy():
                pass
            return 'q', 'q'
        # TODO: background music?

    for projectile in projectiles:
        # create a hit box around the bullet
        projectile_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
        for asteroid in asteroids:
            # create a hit box around the asteroid
            asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
            # if the two hit boxes collide, then remove the projectile and the asteroid
            if projectile_rect.colliderect(asteroid_rect):
                asteroid.boom.play()
                # Remove the projectile and asteroid
                projectiles.remove(projectile)
                asteroids.remove(asteroid)
                # Break out of the inner loop since projectile can only collide with one asteroid at a time
                break
    return projectiles, asteroids


def run_game():
    running = True
    clock = pygame.time.Clock()

    player = Player()
    projectiles = []
    asteroids = []

    while running:
        Settings.screen.fill(BLACK)

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
            player.blaster.play()
            projectiles.append(Projectile(projectile_x, projectile_y))
            player.cooldown_counter = player.projectile_cooldown

        # Generate asteroids randomly
        if random.randint(1, 100) == 1:
            asteroids.append(Asteroid())

        if player.cooldown_counter > 0:
            player.cooldown_counter -= 1

        projectiles = _UpdateBulletProjectiles(projectiles)
        asteroids = _UpdateAsteroids(asteroids)

        projectiles, asteroids, = _CheckCollisions(projectiles, asteroids, player)
        if projectiles == 'q' or asteroids == 'q':
            running = False

        # Draw player
        pygame.draw.rect(Settings.screen, player.color, (player.x, player.y, player.width, player.height))

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    run_game()

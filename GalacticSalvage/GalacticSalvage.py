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
from Player import Player
from Asteroid import Asteroid
from Scoreboard import Scoreboard
from Settings import Settings



# Initialize Pygame
pygame.init()


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


class Star:
    def __init__(self):
        self.color = Settings.WHITE
        self.radius = 1
        # why does this need to be // 7+ to fill the whole screen?
        self.x = random.randint(0, Settings.SCREEN_WIDTH - Settings.SCREEN_HEIGHT // 7)
        self.y = -Settings.SCREEN_HEIGHT  # Start above the screen
        self.yspeed = random.randint(1, 3)

    def draw(self):
        pygame.draw.circle(Settings.screen, self.color, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def OffscreenReset(self):
        if self.y >= Settings.SCREEN_HEIGHT:
            self.y = 0


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
            # TODO: add a score penalty if an asteroid
    return asteroids


def _UpdateStars(stars: List[Star]):
    for star in stars:
        star.draw()
        star.fall()
        star.OffscreenReset()
    return stars


def _CheckCollisions(projectiles: List[Projectile], asteroids: List[Asteroid],
                     player: Player, scoreboard: Scoreboard):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for asteroid in asteroids:
        # create a hit box around the asteroid
        asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
        # if the two hit boxes collide, then remove the projectile and the asteroid
        if player_rect.colliderect(asteroid_rect):
            mx = player.boom.play()
            while mx.get_busy():
                pass
            return 'q', 'q', 'q'
        # TODO: background music?

    for projectile in projectiles:
        # create a hit box around the bullet
        projectile_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
        for asteroid in asteroids:
            # create a hit box around the asteroid
            asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
            # if the two hit boxes collide, then remove the projectile and the asteroid
            if projectile_rect.colliderect(asteroid_rect):
                scoreboard.increase_score()
                asteroid.boom.play()
                # Remove the projectile and asteroid
                projectiles.remove(projectile)
                asteroids.remove(asteroid)
                # Break out of the inner loop since projectile can only collide with one asteroid at a time
                break
    return projectiles, asteroids, scoreboard


def run_game():
    running = True
    clock = pygame.time.Clock()

    player = Player()
    projectiles = []
    asteroids = []
    stars = []
    scoreboard = Scoreboard()

    while running:
        Settings.screen.fill(Settings.BLACK)

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
        
        # Generate stars randomly
        if random.randint(1, 10) == 1:
            stars.append(Star())

        # deincrement the cooldown counter by 1 if it is greater than 0
        if player.cooldown_counter > 0:
            player.cooldown_counter -= 1

        projectiles = _UpdateBulletProjectiles(projectiles)
        asteroids = _UpdateAsteroids(asteroids)
        stars = _UpdateStars(stars)

        projectiles, asteroids, scoreboard = _CheckCollisions(projectiles, asteroids, player, scoreboard)
        if projectiles == 'q' or asteroids == 'q':
            running = False
        # if running check here prevents the game crashing after the player dies,
        if running:
            # Update the scoreboard
            scoreboard.display(Settings.screen)

            # Draw player
            pygame.draw.rect(Settings.screen, player.color, (player.x, player.y, player.width, player.height))

            # Update the display
            pygame.display.update()
            clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    run_game()

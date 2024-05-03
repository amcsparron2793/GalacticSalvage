#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources
from abandoned space stations and derelict ships.
Navigate through asteroid fields, avoid enemy patrols,
and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""
import pygame
from typing import List
import random
from Player import Player, Projectile
from Asteroid import Asteroid
from Scoreboard import Scoreboard
from Settings import Settings, Sounds


class Star:
    def __init__(self):
        self.color = Settings.WHITE
        self.radius = 1
        # why does this need to be // 7+ to fill the whole screen?
        self.x = random.randint(0, Settings.SCREEN_WIDTH - Settings.SCREEN_HEIGHT // 15)
        self.y = -Settings.SCREEN_HEIGHT  # Start above the screen
        self.yspeed = random.randint(1, 3)

    def draw(self):
        pygame.draw.circle(Settings.screen, self.color, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def OffscreenReset(self):
        if self.y >= Settings.SCREEN_HEIGHT:
            self.y = 0


class GalacticSalvage:
    clock = pygame.time.Clock()

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.running = True
        self.player = Player()
        self.projectiles: List[Projectile] = []
        self.asteroids: List[Asteroid] = []
        self.stars: List[Star] = []
        self.scoreboard = Scoreboard()
        self.sounds = Sounds()

    def FireWeapon(self):
        # Fire projectile
        projectile_x = self.player.x + self.player.width // 2 - 2  # Adjusted for projectile width
        projectile_y = self.player.y
        self.sounds.blaster_sound.play()
        self.projectiles.append(Projectile(projectile_x, projectile_y))
        self.player.cooldown_counter = self.player.projectile_cooldown

    def _UpdateBulletProjectiles(self):
        # Update projectiles
        for projectile in self.projectiles:
            projectile.move()
            pygame.draw.rect(Settings.screen, projectile.color,
                             (projectile.x, projectile.y,
                              projectile.width, projectile.height))
            # Remove projectiles that go off-screen
            if projectile.y < 0:
                self.projectiles.remove(projectile)
        return self.projectiles

    def _UpdateAsteroids(self):
        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.move()
            asteroid.draw(Settings.screen)  # Draw the asteroid with rotation
            # Remove asteroids that go off-screen
            if asteroid.y > Settings.SCREEN_HEIGHT:
                self.asteroids.remove(asteroid)
                self.sounds.missed_asteroid_sound.play()
                self.scoreboard.decrease_score()
        return self.asteroids

    def _UpdateStars(self):
        for star in self.stars:
            star.draw()
            star.fall()
            star.OffscreenReset()
        return self.stars

    def _CheckCollisions(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for asteroid in self.asteroids:
            # create a hit box around the asteroid
            asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
            # if the two hit boxes collide, then remove the projectile and the asteroid
            if player_rect.colliderect(asteroid_rect):
                mx = self.sounds.boom_sound.play()
                if mx:
                    while mx.get_busy():
                        pass
                self.running = False
            # TODO: background music?

        for projectile in self.projectiles:
            # create a hit box around the bullet
            projectile_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
            for asteroid in self.asteroids:
                # create a hit box around the asteroid
                asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
                # if the two hit boxes collide, then remove the projectile and the asteroid
                if projectile_rect.colliderect(asteroid_rect):
                    self.scoreboard.increase_score()
                    asteroid.boom.play()
                    # Remove the projectile and asteroid
                    self.projectiles.remove(projectile)
                    self.asteroids.remove(asteroid)
                    # Break out of the inner loop since projectile can only collide with one asteroid at a time
                    break
        return self.projectiles, self.asteroids, self.scoreboard

    def GameLoop(self):
        while self.running:
            Settings.screen.fill(Settings.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                break

            if keys[pygame.K_LEFT]:
                self.player.move_left()

            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            # Check if spacebar is pressed to shoot
            if keys[pygame.K_SPACE] and self.player.cooldown_counter <= 0:
                self.FireWeapon()

            # Generate asteroids randomly
            if random.randint(1, 100) == 1:
                self.asteroids.append(Asteroid())

            # Generate stars randomly
            if random.randint(1, 10) == 1:
                self.stars.append(Star())

            # de-increment the cooldown counter by 1 if it is greater than 0
            if self.player.cooldown_counter > 0:
                self.player.cooldown_counter -= 1
            self._UpdateBulletProjectiles()
            self._UpdateAsteroids()
            self._UpdateStars()

            self._CheckCollisions()

            # if running check here prevents the game crashing after the player dies,
            if self.running:
                # Update the scoreboard
                self.scoreboard.display(Settings.screen)

                # Draw player
                pygame.draw.rect(Settings.screen, self.player.color,
                                 (self.player.x, self.player.y, self.player.width, self.player.height))

                # Update the display
                pygame.display.update()
                self.clock.tick(60)


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.GameLoop()

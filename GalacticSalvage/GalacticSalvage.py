#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources
from abandoned space stations and derelict ships.
Navigate through asteroid fields, avoid enemy patrols,
and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""
import random
from typing import List

import pygame

from Player import Player, Projectile
from Asteroid import Asteroid
from Star import Star
from Scoreboard import Scoreboard
from Settings import Settings, Sounds


class GalacticSalvage:
    clock = pygame.time.Clock()

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.settings = Settings()

        self.running = True
        self.player = Player(self)
        self.projectiles: List[Projectile] = []
        self.asteroids: List[Asteroid] = []
        self.stars: List[Star] = []
        self.scoreboard = Scoreboard()
        self.sounds = Sounds()
        # TODO: add lives (3 missed asteroids?)

    def FireWeapon(self):
        projectile_x = self.player.x + self.player.width // 2 - 2  # Adjusted for projectile width
        projectile_y = self.player.y
        self.sounds.blaster.play()
        self.projectiles.append(Projectile(self, projectile_x, projectile_y))
        self.player.cooldown_counter = self.player.projectile_cooldown

    def _UpdateBulletProjectiles(self):
        # Update projectiles
        for projectile in self.projectiles:
            projectile.move()
            pygame.draw.rect(self.settings.screen, self.settings.bullet_color,
                             (projectile.x, projectile.y,
                              self.settings.bullet_width, self.settings.bullet_height))
            # Remove projectiles that go off-screen
            if projectile.y < 0:
                self.projectiles.remove(projectile)
        return self.projectiles

    def _UpdateAsteroids(self):
        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.move()
            asteroid.draw(self.settings.screen)  # Draw the asteroid with rotation
            # Remove asteroids that go off-screen
            if asteroid.y > self.settings.screen_height:
                self.asteroids.remove(asteroid)
                self.sounds.missed_asteroid.play()
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
                mx = self.sounds.player_boom.play()
                if mx:
                    while mx.get_busy():
                        pass
                self.running = False
            # TODO: background music?

        for projectile in self.projectiles:
            # create a hit box around the bullet
            projectile_rect = pygame.Rect(projectile.x, projectile.y,
                                          self.settings.bullet_width,
                                          self.settings.bullet_height)
            for asteroid in self.asteroids:
                # create a hit box around the asteroid
                asteroid_rect = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
                # if the two hit boxes collide, then remove the projectile and the asteroid
                if projectile_rect.colliderect(asteroid_rect):
                    self.scoreboard.increase_score()
                    self.sounds.asteroid_boom.play()
                    # Remove the projectile and asteroid
                    self.projectiles.remove(projectile)
                    self.asteroids.remove(asteroid)
                    # Break out of the inner loop since projectile can only collide with one asteroid at a time
                    break
        return self.projectiles, self.asteroids, self.scoreboard

    def GameLoop(self):
        while self.running:
            self.settings.screen.fill(Settings.BLACK)

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
                self.asteroids.append(Asteroid(self))

            # Generate stars randomly
            if random.randint(1, 10) == 1:
                self.stars.append(Star(self))

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
                self.scoreboard.display(self.settings.screen)

                # Draw player
                pygame.draw.rect(self.settings.screen, self.player.color,
                                 (self.player.x, self.player.y, self.player.width, self.player.height))

                # Update the display
                pygame.display.update()
                self.clock.tick(60)


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.GameLoop()

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

from Player import Player, Bullet
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
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.stars: List[Star] = []
        self.scoreboard = Scoreboard()
        self.sounds = Sounds()
        self._create_asteroids()
        # TODO: add lives (3 missed asteroids?)

    def _check_keydown_events(self, event):
        """ Respond to key presses. """
        if event.key == pygame.K_RIGHT:
            # move the ship to the right
            self.player.moving_right = True

        elif event.key == pygame.K_LEFT:
            # move the ship to the left
            self.player.moving_left = True

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            # self.sb.write_highscore()
            # if q or esc is pressed quit the game
            self.running = False

        elif event.key == pygame.K_SPACE: #and self.stats.game_active is True:
            self._fire_bullet()
        elif event.key == pygame.K_F12:
            self.settings.ToggleFullscreen()

    def _check_keyup_events(self, event):
        """ Respond to key releases. """
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.blaster.play()

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets. """
        # Update bullet positions.
        self.bullets.update()

        # get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # for debugging this makes sure that the bullets are actually being deleted
        # print(len(self.bullets))
        self._check_bullet_asteroid_collisions()

    def _check_bullet_asteroid_collisions(self):
        """ Respond to bullet asteroid collisions. """
        # Check for any bullets that have hit asteroids.
        # If so, get rid of the bullet and the asteroid.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.asteroids, True, True)

        if collisions:
            for asteroid in collisions.values():
                self.scoreboard.increase_score()
                self.sounds.asteroid_boom.play()
                self.asteroids.remove(asteroid)
                # print(f"score is: {self.scoreboard.score}\n asteroids remaining: {len(self.asteroids)}")
                self._create_asteroids()

    def _create_asteroids(self):
        # Create asteroids and add them to the sprite groups
        if len(self.asteroids) < 1:
            for _ in range(random.randint(1, 5)):  # Adjust the number of asteroids as needed
                asteroid = Asteroid(self)
                self.asteroids.add(asteroid)

    def _update_asteroids(self):
        # Update asteroids
        self.asteroids.update()
        for asteroid in self.asteroids.copy():
            # asteroid.move()
            # asteroid.draw(self.settings.screen)  # Draw the asteroid with rotation
            # print("asteroid drawn")
            # Remove asteroids that go off-screen
            if asteroid.rect.bottom >= self.settings.screen.get_height():
                self.asteroids.remove(asteroid)
                self.sounds.missed_asteroid.play()
                self.scoreboard.decrease_score()
                self._create_asteroids()

    def _UpdateStars(self):
        for star in self.stars:
            star.draw()
            star.fall()
            star.OffscreenReset()
        return self.stars

    def _check_events(self):
        """ Respond to key presses and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """ Update images on the screen and flip to the new screen. """
        self.settings.screen.fill(self.settings.bg_color)
        self.player.biltme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.asteroids.draw(self.settings.screen)

        # Draw the score information
        self.scoreboard.display(self.settings.screen)

        # draw the play button if the game is inactive
        """if not self.stats.game_active:
            self.play_button.draw_button()"""

        # Make the most recently drawn screen visible
        pygame.display.flip()
        self.clock.tick(120)
        # self.clock.tick(60)

    def run_game(self):
        """start the main loop for the game"""
        while self.running:
            self._check_events()
            self.player.update()
            self._update_bullets()
            self._update_asteroids()
            self._UpdateStars()
            self._update_screen()
        pygame.quit()


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.run_game()

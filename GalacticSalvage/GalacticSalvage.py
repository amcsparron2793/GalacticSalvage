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
            # if q or esc is pressed write the highscore file and quit the game
            # sys.exit()
            pygame.quit()

        elif event.key == pygame.K_SPACE: #and self.stats.game_active is True:
            self._fire_bullet()

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
            for asteroids in collisions.values():
                self.scoreboard.increase_score()
                self.sounds.asteroid_boom.play()

    def _UpdateBulletProjectiles(self):
        self.bullets.update()

        # get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_asteroid_collisions()

    def _UpdateAsteroids(self):
        # Update asteroids
        self.asteroids.update()
        """for asteroid in self.asteroids:
            asteroid.move()
            asteroid.draw(self.settings.screen)  # Draw the asteroid with rotation
            # Remove asteroids that go off-screen
            if asteroid.y > self.settings.screen_height:
                self.asteroids.remove(asteroid)
                self.sounds.missed_asteroid.play()
                self.scoreboard.decrease_score()
        return self.asteroids"""

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
        #self.sb.show_score()

        # draw the play button if the game is inactive
        """if not self.stats.game_active:
            self.play_button.draw_button()"""

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()

            self.player.update()
            self._update_bullets()
            self._UpdateAsteroids()
            self._UpdateStars()
            self._update_screen()



    """def GameLoop(self):
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
                self._fire_bullet()

            # Generate asteroids randomly
            if random.randint(1, 100) == 1:
                new_asteroid = Asteroid(self)
                self.asteroids.add(new_asteroid)
                self.asteroids.update()

            # Generate stars randomly
            if random.randint(1, 10) == 1:
                self.stars.append(Star(self))

            # de-increment the cooldown counter by 1 if it is greater than 0
            if self.player.cooldown_counter > 0:
                self.player.cooldown_counter -= 1
            self._UpdateBulletProjectiles()
            self._UpdateAsteroids()
            self._UpdateStars()

            # self._CheckCollisions()

            # if running check here prevents the game crashing after the player dies,
            if self.running:
                # Update the scoreboard
                self.scoreboard.display(self.settings.screen)

                # Draw player
                pygame.draw.rect(self.settings.screen, self.player.color,
                                 (self.player.x, self.player.y, self.player.width, self.player.height))

                # Update the display
                pygame.display.update()
                self.clock.tick(60)"""


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.run_game()

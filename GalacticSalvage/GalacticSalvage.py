#! python3
"""
GalacticSalvage

Players control a spaceship tasked with salvaging valuable resources
from abandoned space stations and derelict ships.
Navigate through asteroid fields, avoid enemy patrols,
and use a variety of retro-inspired weapons and upgrades to fend off hostile forces.
"""

import pygame

import random
from typing import List

try:
    from .Player import Player, Bullet
    from .Asteroid import Asteroid
    from .Star import Star
    from .Scoreboard import Scoreboard, FPSMon
    from .Settings import Settings
    from .Sound import Sounds
    from .Button import Button
    from .PowerupsSpecials import BrokenShip, ExtraLife
    from .Leaderboard import Leaderboard

except ImportError:
    from Player import Player, Bullet
    from Asteroid import Asteroid
    from Star import Star
    from Scoreboard import Scoreboard, FPSMon
    from Settings import Settings
    from Sound import Sounds
    from Button import Button
    from PowerupsSpecials import BrokenShip, ExtraLife
    from Leaderboard import Leaderboard


class GalacticSalvage:
    """
    GalacticSalvage

    This class represents the main game object in the Galactic Salvage game.
    It manages the game state, including player input, game objects, and game logic.

    Attributes:
        clock: The Pygame clock object used to manage the game's frame rate.
        settings: An instance of the Settings class that stores the game's settings.
        level: The current level of the game.
        running: A boolean indicating whether the game is currently running.
        game_active: A boolean indicating whether the game is currently active.
        play_button: An instance of the Button class representing the play button.
        player: An instance of the Player class representing the player's ship.
        bullets: A Pygame sprite Group containing the bullets fired by the player's ship.
        asteroids: A Pygame sprite Group containing the asteroids in the game.
        broken_ships: A Pygame sprite Group containing the broken ships in the game.
        extra_lives: A Pygame sprite Group containing the extra lives in the game.
        stars: A list of Star objects representing the background stars in the game.
        scoreboard: An instance of the Scoreboard class that manages the game's scoreboard.
        fps: An instance of the FPSMon class that displays the game's frame rate.
        sounds: An instance of the Sounds class that manages the game's sound effects.
        mix: The Pygame Mixer object used to play sound effects.
        missed_ship_penalty: The penalty score for missing a broken ship.
        missed_asteroid_penalty: The penalty score for missing an asteroid.
        player_asteroid_hit_penalty: The penalty score for the player's ship colliding with an asteroid.

    Methods:
        __init__(self): Initializes the GalacticSalvage object and sets up the game.
        _check_keydown_events(self, event): Responds to key press events by performing the associated actions.
        _check_keyup_events(self, event): Responds to key release events by performing the associated actions.
        _check_play_button(self, mouse_pos): Starts a new game when the player presses the play button.
        _fire_bullet(self): Creates a new bullet and adds it to the bullets group.
        _update_bullets(self): Updates the position of bullets and removes any old bullets.
        _check_bullet_asteroid_collisions(self): Responds to collisions between bullets and asteroids by removing them from the game.
        _check_asteroid_ship_collisions(self): Responds to collisions between the player's ship and asteroids by performing the associated actions.
        _check_broken_ship_ship_collisions(self): Responds to collisions between the player's ship and broken ships by performing the associated actions.
        _check_extra_life_ship_collisions(self): Responds to collisions between the player's ship and extra lives by performing the associated actions.
        _create_asteroids(self): Creates asteroids and adds them to the sprite groups.
        _update_asteroids(self): Updates the position of asteroids and removes any that go off-screen.
        _create_broken_ship(self): Creates a new broken ship and adds it to the broken ships group.
        _update_broken_ship(self): Updates the position of broken ships and removes any that go off-screen.
        _create_extra_life(self): Creates a new extra life and adds it to the extra lives group.
        _update_extra_life(self): Updates the position of extra lives and removes any that go off-screen.
        _UpdateStars(self): Updates the position of the background stars.
        _check_system_events(self): Responds to system events such as quitting the game or clicking the play button.
        _get_random_events(self): Generates random events such as creating a broken ship or extra life.
    """
    clock = pygame.time.Clock()

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.settings = Settings()
        self.leaderboard = Leaderboard(self)
        self.level = 1

        self.running = True
        self.game_active = False
        self.play_button = Button(self, "Start")
        self.player = Player(self)

        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.broken_ships = pygame.sprite.Group()
        self.extra_lives = pygame.sprite.Group()

        self.stars: List[Star] = []

        self.scoreboard = Scoreboard(self)
        self.fps = FPSMon(self)

        self.sounds = Sounds(self)
        self.mix = self.sounds.mx
        self._create_asteroids()

        self.missed_ship_penalty = 3
        self.missed_asteroid_penalty = 1
        self.player_asteroid_hit_penalty = 5
        self.player_name = self.leaderboard.get_player_name()

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
            # if q or esc is pressed pause the game
            self.game_active = False
            if event.key == pygame.K_q and not self.game_active:
                self.running = False

        elif event.key == pygame.K_SPACE and self.game_active is True:
            self._fire_bullet()
        elif event.key == pygame.K_F12:
            self.settings.ToggleFullscreen()
        elif event.key == pygame.K_m:
            self.sounds.toggle_mute()

    def _check_keyup_events(self, event):
        """ Respond to key releases. """
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player presses play. """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset the game settings
            # reset the game statistics
            self.game_active = True

    # noinspection PyTypeChecker
    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.mix.play(self.sounds.blaster)

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
                self.scoreboard.increase_score(1)
                self.mix.play(self.sounds.asteroid_boom)
                self.asteroids.remove(asteroid)

    def _check_asteroid_ship_collisions(self):
        """ Respond to ship asteroid collisions. """
        # Check for any asteroids that have hit the ship.
        # If so, get rid of the ship and the asteroid.
        collisions = pygame.sprite.spritecollideany(self.player, self.asteroids)

        if collisions:
            if self.scoreboard.score >= self.player_asteroid_hit_penalty:
                self.scoreboard.decrease_score(self.player_asteroid_hit_penalty)
            else:
                self.scoreboard.score = 0

            self.mix.play(self.sounds.player_boom)

            if self.player.player_lives > 0:
                self.player.player_lives -= 1
                self.asteroids.empty()
                self.player.remove()
                self.player.center_ship()
                self.player.biltme()
                # print(f"score is: {self.scoreboard.score}\n asteroids remaining: {len(self.asteroids)}")
            else:
                self.mix.play(self.sounds.player_boom)
                while self.mix.get_busy():
                    pass
                self.mix.play(self.sounds.game_over)
                while self.mix.get_busy():
                    pass
                # TODO: show leaderboard
                self.running = False

    def _check_broken_ship_ship_collisions(self):
        """ Respond to ship broken ship collisions. """
        # Check for any asteroids that have hit the ship.
        # If so, get rid of the ship and the asteroid.
        collisions = pygame.sprite.spritecollideany(self.player, self.broken_ships)

        if collisions:
            self.scoreboard.increase_score(10)
            self.broken_ships.remove(collisions)
            self.mix.play(self.sounds.saved_broken_ship)

    def _check_extra_life_ship_collisions(self):
        """ Respond to ship broken ship collisions. """
        # Check for any asteroids that have hit the ship.
        # If so, get rid of the ship and the asteroid.
        collisions = pygame.sprite.spritecollideany(self.player, self.extra_lives)

        if collisions:
            self.player.player_lives += 1
            self.extra_lives.remove(collisions)
            self.mix.play(self.sounds.saved_broken_ship)

    # noinspection PyTypeChecker
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
            # Remove asteroids that go off-screen
            if asteroid.rect.bottom >= self.settings.screen.get_height():
                self.asteroids.remove(asteroid)
                self.mix.play(self.sounds.missed_asteroid)
                self.scoreboard.decrease_score(self.missed_asteroid_penalty)
                self._create_asteroids()

    def _create_broken_ship(self):
        broken_ship = BrokenShip(self)
        self.broken_ships.add(broken_ship)

    def _update_broken_ship(self):
        self.broken_ships.update()
        for ship in self.broken_ships.copy():
            # Remove asteroids that go off-screen
            if ship.rect.bottom >= self.settings.screen.get_height():
                self.broken_ships.remove(ship)
                self.scoreboard.decrease_score(self.missed_ship_penalty)
                self.mix.play(self.sounds.missed_asteroid)

    def _create_extra_life(self):
        extra_life = ExtraLife(self)
        self.extra_lives.add(extra_life)

    def _update_extra_life(self):
        self.extra_lives.update()
        for life in self.extra_lives.copy():
            if life.rect.bottom >= self.settings.screen.get_height():
                self.extra_lives.remove(life)

    def _UpdateStars(self):
        for star in self.stars:
            star.draw()
            star.fall()
            star.OffscreenReset()
        return self.stars

    def _check_system_events(self):
        """ Respond to key presses and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _get_random_events(self):
        if random.randint(1, 2000) == 1:
            self._create_broken_ship()
        if random.randint(1, 4000) == 1:
            self._create_extra_life()
        if random.randint(1, 100) == 1:
            self._create_asteroids()

    def _draw_sprites(self):
        for life in self.extra_lives.sprites():
            life.draw(self.settings.screen)
        for b_ship in self.broken_ships.sprites():
            b_ship.draw(self.settings.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.asteroids.draw(self.settings.screen)

    def _update_screen(self):
        """ Update images on the screen and flip to the new screen. """
        self._get_random_events()
        self.settings.screen.fill(self.settings.bg_color)
        self.player.biltme()

        self._draw_sprites()

        # Draw the score information
        self.scoreboard.display(self.settings.screen)

        if self.settings.show_fps:
            self.fps.render_fps(self.settings.screen)

        if self.sounds.is_muted:
            self.sounds.draw_mute_img(self.settings.screen)

        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()
        # self.clock.tick(120)
        self.clock.tick(60)

    def _check_level(self):
        if self.scoreboard.score >= self.level * 10:
            self.level += 1
            self.scoreboard.level = self.level
            print(f"LEVEL UP - Level {self.level}")
            self.mix.play(self.sounds.level_up)

    def run_game(self):
        """start the main loop for the game"""
        while self.running:
            self._check_system_events()
            if self.game_active:
                self._check_asteroid_ship_collisions()
                self._check_broken_ship_ship_collisions()
                self._check_extra_life_ship_collisions()
                self.player.update()
                self._update_bullets()
                self._update_asteroids()
                self._update_broken_ship()
                self._update_extra_life()
                self._UpdateStars()
                self._check_level()
            self._update_screen()
        self.leaderboard.add_entry(self.player_name)
        pygame.quit()


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.run_game()

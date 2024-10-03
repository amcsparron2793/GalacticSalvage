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



try:
    from PowerupsSpecials import UnlimitedBulletsPowerUp
    from Bullet import SuperBullet
    from GameInitializer import GameInitializer

except ImportError:
    from .PowerupsSpecials import UnlimitedBulletsPowerUp
    from .Bullet import SuperBullet
    from .GameInitializer import GameInitializer


class GalacticSalvage(GameInitializer):
    """
    Class: GalacticSalvage

    The GalacticSalvage class is responsible for coordinating the gameplay, handling user input, updating game objects, and checking for collisions.

    Attributes:
    - clock: A Pygame clock object used for controlling the frame rate of the game.
    - settings: An instance of the Settings class that stores all the game settings.
    - leaderboard: An instance of the Leaderboard class that manages the leaderboard functionality.
    - show_leaderboard: A boolean flag indicating whether the leaderboard should be displayed.
    - use_superbullet: A boolean flag indicating whether the player is using a super bullet power-up.
    - level: An integer representing the current level.
    - running: A boolean flag indicating whether the game is running.
    - game_active: A boolean flag indicating whether the game is currently being played.
    - play_button: An instance of the Button class representing the play button on the screen.
    - player: An instance of the Player class representing the player's ship.
    - bullets: A Pygame sprite group containing all the bullets fired by the player.
    - persistent_powerups_available: A Pygame sprite group containing all the persistent power-ups available.
    - has_superbullet: A boolean flag indicating whether the player has a super bullet power-up.
    - asteroids: A Pygame sprite group containing all the asteroids in the game.
    - broken_ships: A Pygame sprite group containing all the broken ships in the game.
    - extra_lives: A Pygame sprite group containing all the extra lives in the game.
    - super_bullet_powerups: A Pygame sprite group containing all the super bullet power-ups in the game.
    - stars: A list of Star objects representing the stars in the background.
    - scoreboard: An instance of the Scoreboard class that keeps track of the player's score.
    - fps: An instance of the FPSMon class that displays the current frame rate of the game.
    - sounds: An instance of the Sounds class that manages the game's sound effects.
    - sfx_mix: The Pygame mixer object used for playing sound effects.
    - missed_ship_penalty: An integer representing the penalty for missing a ship.
    - missed_asteroid_penalty: An integer representing the penalty for missing an asteroid.
    - player_asteroid_hit_penalty: An integer representing the penalty for the player being hit by an asteroid.
    - player_name: A string representing the name of the player.

    Methods:
    - __init__(): Initializes the GalacticSalvage object and sets up the initial game state.
    - _check_keydown_events(event): Handles keyboard key down events and responds accordingly.
    - _check_keyup_events(event): Handles keyboard key up events and responds accordingly.
    - _check_play_button(mouse_pos): Checks if the play button was clicked and starts a new game if it was.
    - _fire_bullet(): Creates a new bullet and adds it to the bullets group.
    - _update_bullets(): Updates the position of bullets and removes old bullets from the bullets group.
    - _check_bullet_asteroid_collisions(): Checks for collisions between bullets and asteroids and handles them.
    - _check_asteroid_ship_collisions(): Checks for collisions between asteroids and the player's ship and handles them.
    - _check_broken_ship_ship_collisions(): Checks for collisions between broken ships and the player's ship and handles them.
    - _check_extra_life_ship_collisions(): Checks for collisions between extra lives and the player's ship and handles them.
    - _check_super_bullet_pu_ship_collisions(): Checks for collisions between super bullet power-ups and the player's ship and handles them.
    - _create_asteroids(): Creates new asteroids and adds them to the asteroids group.
    - _update_asteroids(): Updates the position of asteroids and removes off-screen asteroids from the asteroids group.
    - _create_broken_ship(): Creates a new broken ship and adds it to the broken ships group.
    - _update_broken_ship(): Updates the position of broken ships and removes off-screen broken ships from the broken ships group.

    """
    clock = pygame.time.Clock()
    RANDOM_EVENT_ODDS_MAX = {'broken_ship': 2000,
                             'extra_life': 4000,
                             'asteroid': 100,
                             'super_bullet_pu': 3500,
                             'unlimited_bullets_pu': 3500}

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self._initialize_game()
        self.player_name = self.leaderboard.get_player_name()

    def _check_system_events(self):
        """
        Checks for system events and performs corresponding actions.

        This method checks for system events using the `pygame.event.get()` function. It iterates over each event and performs actions based on the event type. The following event types are checked:

        - `pygame.QUIT`: If the event type is `pygame.QUIT`, the `pygame.quit()` function is called to quit the game.
        - `pygame.MOUSEBUTTONDOWN`: If the event type is `pygame.MOUSEBUTTONDOWN`, the current mouse position is obtained using `pygame.mouse.get_pos()` and passed to the `_check_play_button()` method.
        - `pygame.KEYDOWN`: If the event type is `pygame.KEYDOWN`, the event is passed to the `_check_keydown_events()` method.
        - `pygame.KEYUP`: If the event type is `pygame.KEYUP`, the event is passed to the `_check_keyup_events()` method.

        This method should be called in the game loop to continuously check for system events.

        """
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
        """
        This method generates random events for the game.

        It uses the random module to generate random numbers and based on the generated numbers, it calls different private methods to create specific game events.

        Example usage:
            game = Game()
            game._get_random_events()

            Here, the _get_random_events() method is called on an instance of the Game class to generate random events for the game.

        Note:
        - This method is for internal use and should not be called directly from outside the class.
        - The probabilities for the random events are hardcoded and can be adjusted as needed.
        """
        if random.randint(1, self.RANDOM_EVENT_ODDS_MAX['broken_ship']) == 1:
            self._create_broken_ship()
        if random.randint(1, self.RANDOM_EVENT_ODDS_MAX['extra_life']) == 1:
            self._create_extra_life()
        if random.randint(1, self.RANDOM_EVENT_ODDS_MAX['asteroid']) == 1:
            self._create_asteroids()
        if random.randint(1, self.RANDOM_EVENT_ODDS_MAX['super_bullet_pu']) == 1:
            self._create_super_bullet_pu()
        if random.randint(1, self.RANDOM_EVENT_ODDS_MAX['unlimited_bullets_pu']) == 1:
            self._create_unlimited_bullet_pu()

    def _draw_sprites(self):
        """
        Function name: _draw_sprites

        Description:
        This function is responsible for drawing the various sprites on the game screen.

        Parameters:
        - None

        Returns:
        - None

        """
        for sb_power_up in self.super_bullet_powerups.sprites():
            sb_power_up.draw(self.settings.screen)
        for life in self.extra_lives.sprites():
            life.draw(self.settings.screen)
        for b_ship in self.broken_ships.sprites():
            b_ship.draw(self.settings.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for star in self.stars:
            star.draw()
        for unl_bullet in self.unlimited_bullets_powerups.sprites():
            unl_bullet.draw(self.settings.screen)
        self.asteroids.draw(self.settings.screen)

    def _check_saved_powerups(self):
        """
        Checks the saved powerups for any powerup that should no longer be available and removes them from the available powerups list if necessary.

        Args:
            None

        Returns:
            None

        Raises:
            None

        Notes:
            - This method should be called to update the list of available powerups after any changes to the powerup system.
        """
        for powerup in self.persistent_powerups_available.copy():
            if not self.has_superbullet:
                # TODO: if any new powerups are added then they need to be checked here
                if isinstance(powerup, SuperBullet):
                    self.persistent_powerups_available.remove(powerup)
            if not self.has_unlimited_bullet:
                if isinstance(powerup, UnlimitedBulletsPowerUp):
                    self.persistent_powerups_available.remove(powerup)

    def _update_screen(self):
        """
        Updates the screen by performing the following actions:

        - Calls the `_get_random_events()` method to get random events
        - Fills the screen with the background color specified in the settings
        - Draws the player on the screen using the `biltme()` method
        - Draws all the sprites on the screen using the `_draw_sprites()` method
        - Checks for saved power-ups using the `_check_saved_powerups()` method
        - Displays the score information using the `display()` method of the scoreboard
        - Renders and displays the frames per second (FPS) if the `show_fps` setting is enabled
        - Draws the mute image if the game sounds are muted
        - Draws the play button if the game is inactive
        - Makes the most recently drawn screen visible
        - Limits the frame rate to 60 frames per second using the `tick()` method of the `clock` object
        """
        self._get_random_events()
        self.settings.screen.fill(self.settings.bg_color)
        self.player.biltme()

        self._draw_sprites()
        self._check_saved_powerups()

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
        """
        Checks the current level based on the score and updates the level accordingly.

        This method compares the current score with a threshold value calculated as the current level multiplied by 10.
        If the score is greater than or equal to the threshold value, the level is incremented by 1, and
        the scoreboard's level property is updated with the new level value.
        Additionally, a "LEVEL UP" message is printed to the console along with the new level number.
        Finally, a sound effect is played using the sfx_mix object's play method.

        Returns:
            None

        Raises:
            None
        """
        if self.scoreboard.score >= self.level * 10:
            self.level += 1
            self.scoreboard.level = self.level
            print(f"LEVEL UP - Level {self.level}")
            self.sfx_mix.play(self.sounds.level_up)

    def _display_leaderboard(self):
        """
        This method is used to display the leaderboard on the game screen.

        Parameters:
        None

        Returns:
        None

        Behaviour:
        1. Clears the game screen.
        2. Checks if the leaderboard needs to be displayed.
        3. If yes, retrieves the final leaderboard strings from the leaderboard object.
        4. Renders each leaderboard line as text using the scoreboard font and the white color.
        5. Blits each text surface to the game screen at the specified coordinates.
        6. Updates the display to show the rendered leaderboard.
        7. Caps the frame rate to 60 frames per second using the clock object.

        Note:
        - The method assumes that the settings, leaderboard, scoreboard, screen, bg_color, WHITE, clock, and font variables are already defined and accessible.
        - The method requires the Pygame library to be installed.

        Example Usage:
        # Create an instance of the game
        game = Game()

        # Display the leaderboard
        game._display_leaderboard()
        """
        # Clear the screen
        self.settings.screen.fill(self.settings.bg_color)
        if self.show_leaderboard:
            # Display leaderboard
            leaderboard_lines = self.leaderboard.get_final_leaderboard_strings()
            for i, line in enumerate(leaderboard_lines):
                text_surface = self.scoreboard.font.render(line, True, self.settings.WHITE)
                self.settings.screen.blit(text_surface, (50, 50 + i * 40))
            # Update the display
            pygame.display.flip()

            # Cap the frame rate - this needs to be done so that crazy amounts of system resources
            # aren't used to render a static image at 10000000000s of FPS
            self.clock.tick(60)

    @property
    def shooting_accuracy(self):
        return round((self.total_bullets_hit / self.total_bullets_fired) * 100, 2)


    def _update_screen_elements(self):
        self.player.update()
        self._update_bullets()
        self._update_asteroids()
        self._update_broken_ship()
        self._update_extra_life()
        self._update_super_bullet_pu()
        self._update_unlimited_bullet_pu()
        self._update_stars()

    def run_game(self):
        """
        Runs the game loop until the game is over.

        This method is responsible for driving the game logic and updating the game state.
        It repeatedly checks for user input, checks for collisions, updates the game objects, and
        updates the screen to display the updated game state.

        Once the game is over, it displays the leaderboard and allows the player to enter their name.

        After that, it quits the pygame module and exits the program.

        Note:
            - The game loop will continue as long as the `running` attribute of the game object is `True`.
            - The game will only update the game state and display the leaderboard if the `game_active` attribute is `True`.

        """
        while self.running:
            self._check_system_events()
            if self.game_active:
                self._check_all_collisions()
                self._update_screen_elements()
                self._check_level()
            self._update_screen()
        if self.scoreboard.score > 0:
            self.leaderboard.add_entry(self.player_name)

        self.show_leaderboard = True
        print(self.shooting_accuracy)
        while True:
            self._display_leaderboard()
            self._check_system_events()
            if not self.show_leaderboard:
                break

        pygame.quit()


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.run_game()

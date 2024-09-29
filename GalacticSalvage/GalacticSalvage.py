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
    from .Player import Player
    from .Bullet import Bullet, SuperBullet
    from .Asteroid import Asteroid
    from .Star import Star
    from .Scoreboard import Scoreboard, FPSMon
    from .Settings import Settings
    from .Sound import Sounds
    from .Button import Button
    from .PowerupsSpecials import BrokenShip, ExtraLife, SuperBulletPowerUp
    from .Leaderboard import Leaderboard

except ImportError:
    from Player import Player
    from Bullet import Bullet, SuperBullet
    from Asteroid import Asteroid
    from Star import Star
    from Scoreboard import Scoreboard, FPSMon
    from Settings import Settings
    from Sound import Sounds
    from Button import Button
    from PowerupsSpecials import BrokenShip, ExtraLife, SuperBulletPowerUp
    from Leaderboard import Leaderboard


class GalacticSalvage:
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
                         'super_bullet_pu': 3500}

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.settings = Settings()
        self.leaderboard = Leaderboard(self)
        self.show_leaderboard = False

        self.use_superbullet = False
        self.level = 1

        self.running = True
        self.game_active = False
        self.play_button = Button(self, "Start")
        self.player = Player(self)

        self.bullets = pygame.sprite.Group()
        self.persistent_powerups_available = pygame.sprite.Group()
        # FIXME: just for testing
        # self.persistent_powerups_available.add(SuperBullet(self))

        self.has_superbullet = any([isinstance(x, SuperBullet) for x in self.persistent_powerups_available])
        self.asteroids = pygame.sprite.Group()
        self.broken_ships = pygame.sprite.Group()
        self.extra_lives = pygame.sprite.Group()
        self.super_bullet_powerups = pygame.sprite.Group()

        self.stars: List[Star] = [Star(self) for _ in range(25)]
        self.scoreboard = Scoreboard(self)
        self.fps = FPSMon(self)

        self.sounds = Sounds(self)
        self.sfx_mix = self.sounds.sfx_audio_channel
        self.music_mixer = self.sounds.music_mixer
        self.music_mixer.play(-1)

        self._create_asteroids()

        self.missed_ship_penalty = 3
        self.missed_asteroid_penalty = 1
        self.player_asteroid_hit_penalty = 5
        self.player_name = self.leaderboard.get_player_name()

    def _check_keydown_events(self, event):
        """
        This method is responsible for handling keydown events in the game.

        Args:
            event (pygame.event.Event): The keydown event captured by the game.

        Returns:
            None

        Raises:
            None

        Example:
            _check_keydown_events(event)
        """
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
                self.show_leaderboard = False

        elif (event.key == pygame.K_LCTRL and self.game_active is True
              and self.has_superbullet):
            self.sfx_mix.play(self.sounds.saved_broken_ship)
            self.use_superbullet = True

        elif event.key == pygame.K_SPACE and self.game_active is True:
            self._fire_bullet()
            self.use_superbullet = False

        elif event.key == pygame.K_F12:
            self.settings.ToggleFullscreen()
        elif event.key == pygame.K_m:
            self.sounds.toggle_mute()

    def _check_keyup_events(self, event):
        """
        This method is responsible for handling key-up events in the game.

        :param event: The key-up event that is triggered
        :type event: pygame.event.Event
        """
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False

    def _check_play_button(self, mouse_pos):
        """

        Check if the play button is clicked.

        Parameters:
        - `mouse_pos` : tuple
            The x and y coordinates of the mouse position.

        Returns:
        - None

        Behavior:
        - Checks if the play button is clicked by comparing the mouse position with the rectangle of the play button.
        - If the play button is clicked and the game is not active, it resets the game settings and statistics and sets `game_active` to True.

        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset the game settings
            # reset the game statistics
            self.game_active = True

    # noinspection PyTypeChecker
    def _fire_bullet(self):
        """
        Function _fire_bullet(self) is a private method that is responsible for firing bullets in the game.
        It checks if the number of bullets currently on the screen is less than the maximum allowed number of bullets set in the game settings.
        If it is, it checks if the player has the ability to use a superbullet and if they have any superbullets remaining.
        If both conditions are met, a new SuperBullet object is created and added to the bullets group, and the player's superbullet count is reduced by 1.
        If the conditions are not met, a new Bullet object is created and added to the bullets group.

        Parameters:
        - self: The instance of the class that this method belongs to.

        Returns:
        This method does not return any value.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            if self.use_superbullet and self.has_superbullet:
                new_bullet = SuperBullet(self)
                self.has_superbullet = False

            else:
                new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sfx_mix.play(self.sounds.blaster)

    def _update_bullets(self):
        """
        This function updates the positions of the bullets and removes any bullets that have disappeared.
        It also checks for collisions between bullets and asteroids.

        Parameters:
            - None

        Returns:
            - None
        """
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
        """
        Checks for any collisions between bullets and asteroids, and handles the consequences if a collision occurs.

        This method uses the `pygame.sprite.groupcollide` function to detect collisions between two sprite groups, `self.bullets` and `self.asteroids`. The `groupcollide` function returns a dictionary of collisions, where the keys are bullets that collided with asteroids, and the values are the asteroids that were hit by each bullet.

        If there are any collisions detected, the method iterates over the values of the collisions dictionary (which represents the asteroids hit by bullets). For each asteroid, the following actions are performed:
        - The player's score is increased by 1 using the `increase_score` method of `self.scoreboard`.
        - The destruction sound effect is played using the `play` method of `self.sfx_mix`, with the sound specified as `self.sounds.asteroid_boom`.
        - The asteroid is removed from the `self.asteroids` sprite group using the `remove` method.

        Note: This method assumes that the `self.scoreboard`, `self.sfx_mix`, and `self.sounds` variables have been initialized properly beforehand.

        This method makes use of the following imported modules:
        - `pygame.sprite`: Used to detect collisions between sprites.

        This method does not return any values.
        """

        was_superbullet_hit = any([isinstance(b, SuperBullet) for b in self.bullets])
        num_asteroids_on_screen = len(self.asteroids) // 2

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.asteroids, True, True)

        if collisions:
            for asteroid in collisions.values():
                if was_superbullet_hit:
                    self.scoreboard.increase_score(num_asteroids_on_screen)
                else:
                    self.scoreboard.increase_score(1)
                self.sfx_mix.play(self.sounds.asteroid_boom)
                self.asteroids.remove(asteroid)

    def _check_asteroid_ship_collisions(self):
        """
        This method is responsible for checking if any asteroids have collided with the player's ship. If a collision occurs, the method handles the necessary actions such as updating the scoreboard, decreasing player lives, resetting the ship's position, and playing sound effects.

        Parameters:
            - None

        Returns:
            - None

        Side Effects:
            - Modifies the player's score
            - Modifies the player's lives
            - Modifies the player's ship position
            - Modifies the asteroid sprite group
            - Plays sound effects

        Example Usage:
            _check_asteroid_ship_collisions()
        """
        # Check for any asteroids that have hit the ship.
        # If so, get rid of the ship and the asteroid.
        collisions = pygame.sprite.spritecollideany(self.player, self.asteroids)

        if collisions:
            if self.scoreboard.score >= self.player_asteroid_hit_penalty:
                self.scoreboard.decrease_score(self.player_asteroid_hit_penalty)
            else:
                self.scoreboard.score = 0

            self.sfx_mix.play(self.sounds.player_boom)

            if self.player.player_lives > 0:
                self.player.player_lives -= 1
                self.asteroids.empty()
                self.player.remove()
                self.player.center_ship()
                self.player.biltme()
                # print(f"score is: {self.scoreboard.score}\n asteroids remaining: {len(self.asteroids)}")
            else:
                self.sfx_mix.play(self.sounds.player_boom)
                while self.sfx_mix.get_busy():
                    pass
                self.sfx_mix.play(self.sounds.game_over)
                while self.sfx_mix.get_busy():
                    pass
                self.running = False

    def _check_broken_ship_ship_collisions(self):
        """
        Checks for collisions between the player's ship and any broken ships. If a collision is detected, the player's score is increased by 10, the broken ship is removed from the group of broken ships, and a sound effect is played.

        This function does not return any value.
        """
        # Check for any asteroids that have hit the ship.
        # If so, get rid of the ship and the asteroid.
        collisions = pygame.sprite.spritecollideany(self.player, self.broken_ships)

        if collisions:
            self.scoreboard.increase_score(10)
            self.broken_ships.remove(collisions)
            self.sfx_mix.play(self.sounds.saved_broken_ship)

    def _check_extra_life_ship_collisions(self):
        """
        Checks for any collisions between the player's ship and extra life sprites.
        If a collision is detected, the player's number of lives is increased by 1 and the extra life sprite is removed from the game.

        :return: None
        """
        # Check for any extra lives that have hit the ship.
        # If so, get rid of the extra life sprite and add an extra life.
        collisions = pygame.sprite.spritecollideany(self.player, self.extra_lives)

        if collisions:
            self.player.player_lives += 1
            self.extra_lives.remove(collisions)
            self.sfx_mix.play(self.sounds.saved_broken_ship)

    def _check_super_bullet_pu_ship_collisions(self):
        """
        Checks for collisions between the player ship and super bullet powerups.

        If there is a collision, the super bullet powerup sprite is removed and an extra life is added to the game.

        Note:
        - This method relies on the `pygame.sprite.spritecollideany()` function to check for collisions.
        - The `self.player` attribute refers to the player ship sprite.
        - The `self.super_bullet_powerups` attribute holds a group of super bullet powerup sprites.
        - The `self.persistent_powerups_available` attribute holds a group of persistent powerup sprites.
        - The `SuperBullet` class is used to create a new super bullet powerup sprite.
        - The `self.sfx_mix` object is used to play a sound effect when a collision occurs.
        - The `self.sounds.saved_broken_ship` attribute holds the sound effect for a saved broken ship.

        Parameters:
            None

        Returns:
            None
        """
        # Check for any extra lives that have hit the ship.
        # If so, get rid of the extra life sprite and add an extra life.
        collisions = pygame.sprite.spritecollideany(self.player, self.super_bullet_powerups)

        if collisions:
            self.super_bullet_powerups.remove(collisions)
            self.persistent_powerups_available.add(SuperBullet(self))
            self.sfx_mix.play(self.sounds.saved_broken_ship)

    # noinspection PyTypeChecker
    def _create_asteroids(self):
        """
        This method is used to create asteroids and add them to the sprite groups.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None.

        Example Usage:
            create_asteroids(self)
        """
        # Create asteroids and add them to the sprite groups
        if len(self.asteroids) < 1:
            for _ in range(random.randint(1, 5)):  # Adjust the number of asteroids as needed
                asteroid = Asteroid(self)
                self.asteroids.add(asteroid)

    def _update_asteroids(self):
        """
        Updates the asteroids in the game.

            This method updates the position of the asteroids on the screen.
            It first calls the `update()` method on the `self.asteroids` group object to update the position
            of each individual asteroid.
            It then checks if any asteroid has gone off-screen, and if so, removes it from the group,
            plays the `missed_asteroid` sound effect, decreases the player's score by `missed_asteroid_penalty`,
            and creates new asteroids to replace the ones that were removed.

            Args:
                None

            Returns:
                None

        """
        # Update asteroids
        self.asteroids.update()
        for asteroid in self.asteroids.copy():
            # Remove asteroids that go off-screen
            if asteroid.rect.bottom >= self.settings.screen.get_height():
                self.asteroids.remove(asteroid)
                self.sfx_mix.play(self.sounds.missed_asteroid)
                self.scoreboard.decrease_score(self.missed_asteroid_penalty)
                self._create_asteroids()

    def _create_broken_ship(self):
        """
        This method is used to create a broken ship and add it to the set of broken ships in the current object.

        Parameters:
            - None

        Returns:
            - None

        Example:

            # Create a new instance of the class
            obj = ClassName()

            # Call the method to create a broken ship
            obj._create_broken_ship()

        Note:
            - This method should only be called from within the class.
        """
        broken_ship = BrokenShip(self)
        self.broken_ships.add(broken_ship)

    def _update_broken_ship(self):
        """
        Updates the broken ships on the screen and removes any that go off-screen.

        - Method name: _update_broken_ship
        - Parameters: self
        - Return value: None

        This method is responsible for updating the position of the broken ships on the screen and removing any that have gone off-screen. It is called internally and should not be called directly from outside the class.

        The method performs the following steps:
        1. Calls the `update()` method of the `broken_ships` group to update the positions of all the broken ships.
        2. Iterates over a copy of the `broken_ships` group using a for loop.
        3. Checks if the bottom of the ship's rectangle is greater than or equal to the height of the screen. If it is, it means the ship has gone off-screen.
        4. If the ship has gone off-screen, it is removed from the `broken_ships` group.
        5. Decreases the score on the `scoreboard` instance by the `missed_ship_penalty` amount using the `decrease_score()` method.
        6. Plays the `missed_asteroid` sound effect using the `play()` method of the `sfx_mix` instance.

        Note that this method modifies the `broken_ships` group, the `scoreboard` instance, and the audio output.

        Example usage:
            # Assuming an instance of the class has been created already
            instance._update_broken_ship()

        """
        self.broken_ships.update()
        for ship in self.broken_ships.copy():
            # Remove asteroids that go off-screen
            if ship.rect.bottom >= self.settings.screen.get_height():
                self.broken_ships.remove(ship)
                self.scoreboard.decrease_score(self.missed_ship_penalty)
                self.sfx_mix.play(self.sounds.missed_asteroid)

    def _create_extra_life(self):
        """
        Creates an extra life.

        This method is a private method that is intended to be called internally within the class. It creates an instance of the `ExtraLife` object and adds it to the `extra_lives` attribute, which is a set of all active extra lives.

        Parameters:
            self: The current instance of the class.

        Returns:
            None
        """
        extra_life = ExtraLife(self)
        self.extra_lives.add(extra_life)

    def _update_extra_life(self):
        """
        Updates the position of extra life icons.

        The method `_update_extra_life` is responsible for updating the position of the extra life icons on the screen. It is a private method that is called internally by the class.

        Parameters:
            - None

        Returns:
            - None

        Behavior:
            - The method iterates over each extra life icon in the `extra_lives` group.
            - For each icon, the method checks if the icon has reached or passed the bottom of the screen.
            - If an icon has reached or passed the bottom of the screen, it is removed from the `extra_lives` group.

        Side Effects:
            - The position of the extra life icons is updated.
            - Extra life icons that have reached or passed the bottom of the screen are removed from the `extra_lives` group.

        Exceptions:
            - None
        """
        self.extra_lives.update()
        for life in self.extra_lives.copy():
            if life.rect.bottom >= self.settings.screen.get_height():
                self.extra_lives.remove(life)

    def _create_super_bullet_pu(self):
        """
        Creates a Super Bullet Power Up.

        This method is responsible for creating a Super Bullet Power Up object and adding it to the 'super_bullet_powerups' set. After creating the Super Bullet Power Up, the 'has_superbullet' attribute is set to True.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        super_bullet_pu = SuperBulletPowerUp(self)
        self.super_bullet_powerups.add(super_bullet_pu)
        self.has_superbullet = True

    def _update_super_bullet_pu(self):
        """
        Updates the position of the super bullet power-ups and removes any that have reached the bottom of the screen.

        Parameters:
            - None

        Returns:
            - None
        """
        self.super_bullet_powerups.update()
        for pu in self.super_bullet_powerups.copy():
            if pu.rect.bottom >= self.settings.screen.get_height():
                self.super_bullet_powerups.remove(pu)

    def _UpdateStars(self):
        """
        This method updates the state of all stars in the star field.

        It iterates through each star in the star field and performs the following actions:
        - Calls the `draw()` method of the star to draw it on the screen.
        - Calls the `fall()` method of the star to make it fall down.
        - Calls the `reset_offscreen()` method of the star to reset its position if it goes off the screen.

        After iterating through all stars, it returns the updated list of stars.

        Parameters:
            None

        Returns:
            List: The updated list of stars after performing the state update.

        """
        for star in self.stars:
            star.draw()
            star.fall()
            star.reset_offscreen()
        return self.stars

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

    def _check_all_collisions(self):
        self._check_asteroid_ship_collisions()
        self._check_broken_ship_ship_collisions()
        self._check_extra_life_ship_collisions()
        self._check_super_bullet_pu_ship_collisions()

    def _update_screen_elements(self):
        self.player.update()
        self._update_bullets()
        self._update_asteroids()
        self._update_broken_ship()
        self._update_extra_life()
        self._update_super_bullet_pu()
        self._UpdateStars()

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
        while True:
            self._display_leaderboard()
            self._check_system_events()
            if not self.show_leaderboard:
                break

        pygame.quit()


if __name__ == '__main__':
    gs = GalacticSalvage()
    gs.run_game()

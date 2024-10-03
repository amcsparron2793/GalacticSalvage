from datetime import timedelta
from datetime import datetime
import pygame
from typing import List
import random


try:
    from .Player import Player
    from .Bullet import Bullet, SuperBullet
    from .Asteroid import Asteroid
    from .Star import Star
    from .Scoreboard import Scoreboard, FPSMon
    from .Settings import Settings
    from .Sound import Sounds
    from .Button import Button
    from .PowerupsSpecials import BrokenShip, ExtraLife, SuperBulletPowerUp, UnlimitedBulletsPowerUp
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
    from PowerupsSpecials import BrokenShip, ExtraLife, SuperBulletPowerUp, UnlimitedBulletsPowerUp
    from Leaderboard import Leaderboard


# noinspection PyUnresolvedReferences
class _HIDEventHandler:
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
        elif self._is_unlimited_bullets_enabled(event):
            self.sfx_mix.play(self.sounds.saved_broken_ship)
            self.use_unlimited_bullets = True

        elif self._is_superbullet_enabled(event):
            self.sfx_mix.play(self.sounds.saved_broken_ship)
            self.use_superbullet = True

        elif event.key == pygame.K_SPACE and self.game_active is True:
            self._fire_bullet()
            self.use_superbullet = False

        elif event.key == pygame.K_F12:
            self.settings.toggle_fullscreen()
        elif event.key == pygame.K_m:
            self.sounds.toggle_mute()

    def _is_unlimited_bullets_enabled(self, event):
        return (event.key == pygame.K_RCTRL
                and self.game_active
                and self.has_unlimited_bullet)

    def _is_superbullet_enabled(self, event):
        return (event.key == pygame.K_LCTRL
                and self.game_active
                and self.has_superbullet)

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
            if self.unlimited_bullet_start_time:
                ub_timer = timedelta(seconds=datetime.now().timestamp() - self.unlimited_bullet_start_time)
                if ub_timer >= self.unlimited_bullets_timer_limit:
                    self.settings.bullets_allowed = 3
                    self.use_unlimited_bullets = False
                    self.has_unlimited_bullet = False
                    self.unlimited_bullet_start_time = None


            if self.use_superbullet and self.has_superbullet:
                new_bullet = SuperBullet(self)
                self.has_superbullet = False
            elif self.use_unlimited_bullets and self.has_unlimited_bullet:
                if not self.unlimited_bullet_start_time:
                    self.unlimited_bullet_start_time = datetime.now().timestamp()
                self.settings.bullets_allowed = 9999
                new_bullet = Bullet(self)

            else:
                new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.total_bullets_fired += 1
            self.sfx_mix.play(self.sounds.blaster)


# noinspection PyUnresolvedReferences
class CollisionHandler:
    def _add_powerup_to_scoreboard(self, powerup):
        if not any([isinstance(x, powerup) for x in self.persistent_powerups_available]):
            self.persistent_powerups_available.add(powerup(self))

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
                    self.total_bullets_hit += 1
                    self.sfx_mix.play(self.sounds.asteroid_boom)
                self.asteroids.remove(asteroid)


    def _check_asteroid_ship_collisions(self):
        """
        This method is responsible for checking if any asteroids have collided with the player's ship.
        If a collision occurs, the method handles the necessary actions such as updating the scoreboard,
        decreasing player lives, resetting the ship's position, and playing sound effects.

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
        # If so, get rid of the sprite and add the powerup.
        collisions = pygame.sprite.spritecollideany(self.player, self.super_bullet_powerups)

        if collisions:
            self.super_bullet_powerups.remove(collisions)
            self._add_powerup_to_scoreboard(SuperBullet)
            self.sfx_mix.play(self.sounds.saved_broken_ship)

    def _check_unlimited_bullets_pu_ship_collisions(self):
        """
        Checks for collisions between the player ship and unlimited_bullets powerups.

        If there is a collision, the super bullet powerup sprite is removed and an extra life is added to the game.

        Note:
        - This method relies on the `pygame.sprite.spritecollideany()` function to check for collisions.
        - The `self.player` attribute refers to the player ship sprite.
        - The `self.unlimited_bullets` attribute holds a group of super bullet powerup sprites.
        - The `self.persistent_powerups_available` attribute holds a group of persistent powerup sprites.
        - The `UnlimitedBullets` class is used to create a new unlimited bullets powerup sprite.
        - The `self.sfx_mix` object is used to play a sound effect when a collision occurs.
        - The `self.sounds.saved_broken_ship` attribute holds the sound effect for a saved broken ship.

        Parameters:
            None

        Returns:
            None
        """
        # Check for any extra lives that have hit the ship.
        # If so, get rid of the sprite and add the powerup.
        collisions = pygame.sprite.spritecollideany(self.player, self.unlimited_bullets_powerups)

        if collisions:
            self.unlimited_bullets_powerups.remove(collisions)
            self._add_powerup_to_scoreboard(UnlimitedBulletsPowerUp)
            self.sfx_mix.play(self.sounds.saved_broken_ship)

    def _check_all_collisions(self):
        self._check_asteroid_ship_collisions()
        self._check_broken_ship_ship_collisions()
        self._check_extra_life_ship_collisions()
        self._check_super_bullet_pu_ship_collisions()
        self._check_unlimited_bullets_pu_ship_collisions()


# noinspection PyUnresolvedReferences
class _CreateUpdateSprites:
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

    def _create_unlimited_bullet_pu(self):
        """
        Creates an Unlimited Bullet Power Up.

        This method is responsible for creating an Unlimited Bullet Power Up object and adding it
         to the 'unlimited_bullet_powerups' set.
         After creating the Unlimited Bullet Power Up, the 'has_unlimited' attribute is set to True.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """

        self.unlimited_bullets_powerups.add(UnlimitedBulletsPowerUp(self))
        self.has_unlimited_bullet = True

    def _update_unlimited_bullet_pu(self):
        """
        Updates the position of the super bullet power-ups and removes any that have reached the bottom of the screen.

        Parameters:
            - None

        Returns:
            - None
        """
        self.unlimited_bullets_powerups.update()
        for pu in self.unlimited_bullets_powerups.copy():
            if pu.rect.bottom >= self.settings.screen.get_height():
                self.unlimited_bullets_powerups.remove(pu)


    def _update_stars(self):
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


class GameInitializer(_HIDEventHandler, CollisionHandler, _CreateUpdateSprites):
    def _initialize_game(self):
        self.settings = Settings()
        self.level = 1
        self.unlimited_bullet_start_time = None
        self.unlimited_bullets_timer_limit  = timedelta(seconds=10)
        self.total_bullets_fired = 0
        self.total_bullets_hit = 0

        self._initialize_sprite_groups()
        self._initialize_bools()
        self._initialize_sound()
        self._initialize_miss_penalties()
        self._initialize_helper_classes()
        self._create_asteroids()

    def _initialize_miss_penalties(self):
        self.missed_ship_penalty = 3
        self.missed_asteroid_penalty = 1
        self.player_asteroid_hit_penalty = 5

    def _initialize_helper_classes(self):
        self.leaderboard = Leaderboard(self)
        self.play_button = Button(self, "Start")
        self.player = Player(self)
        self.scoreboard = Scoreboard(self)
        self.fps = FPSMon(self)

    def _initialize_bools(self):
        self.show_leaderboard = False
        self.use_superbullet = False
        self.use_unlimited_bullets = False
        self.running = True
        self.game_active = False
        self.has_superbullet = any((isinstance(x, SuperBullet) for x in self.persistent_powerups_available))
        self.has_unlimited_bullet = any((isinstance(x, UnlimitedBulletsPowerUp) for x in self.persistent_powerups_available))

    def _initialize_sound(self):
        self.sounds = Sounds(self)
        self.sfx_mix = self.sounds.sfx_audio_channel
        self.music_mixer = self.sounds.music_mixer
        self.music_mixer.play(-1)

    def _initialize_sprite_groups(self):
        self.bullets = pygame.sprite.Group()
        self.persistent_powerups_available = pygame.sprite.Group()
        # FIXME: just for testing
        # self.persistent_powerups_available.add(SuperBullet(self))

        self.asteroids = pygame.sprite.Group()
        self.broken_ships = pygame.sprite.Group()
        self.extra_lives = pygame.sprite.Group()
        self.super_bullet_powerups = pygame.sprite.Group()
        self.unlimited_bullets_powerups = pygame.sprite.Group()
        self.stars: List[Star] = [Star(self) for _ in range(25)]
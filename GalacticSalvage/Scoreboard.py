from pathlib import Path

from pygame import font, image, transform


class Scoreboard:
    """
    Class to manage the scoreboard in a game.

    Attributes:
        settings (GameSettings): The game settings object.
        level (int): The current level of the game.
        player (Player): The player object in the game.
        score (int): The current score of the player.
        font (pygame.font.Font): The font used to render the scoreboard text.
        color (tuple): The color of the scoreboard text.
        player_lives_image (pygame.Surface): The image representing the player lives.
    """
    PLAYER_LIVES_IMAGE_PATH = Path('../Misc_Project_Files/images/PlayerShipNoBackground.png')
    SUPER_BULLET_IMAGE_PATH = Path('../Misc_Project_Files/images/SuperBullet.png')
    UNLIMITED_BULLETS_IMAGE_PATH = Path('../Misc_Project_Files/images/UnlimitedBullets.png')
    SCORE_TEXT_LOCATION_TUPLE = (10, 10)
    LIFE_TEXT_LOCATION_TUPLE = (1, 65)
    LIFE_IMAGE_LOCATION_TUPLE = (1, 75)
    POWERUP_TITLE_TEXT_LOCATION_TUPLE = (1, 125)
    FIRST_POWERUP_LOCATION_TUPLE = (1, 135)



    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.level = gs_game.level
        self.player = gs_game.player
        self.leaderboard = gs_game.leaderboard
        self.persistent_powerups_available = gs_game.persistent_powerups_available
        self.score = 0
        self.font = font.SysFont(self.settings.scoreboard_font_name,
                                 self.settings.scoreboard_font_size)
        self.color = self.settings.scoreboard_font_color

        self.player_lives_image = transform.scale_by(image.load(self.PLAYER_LIVES_IMAGE_PATH), 0.05)
        self.super_bullet_image = image.load(self.SUPER_BULLET_IMAGE_PATH)
        self.unlimited_bullets_image = transform.scale_by(image.load(self.UNLIMITED_BULLETS_IMAGE_PATH),0.75)

    def increase_score(self, amount=1):
        self.score += amount

    def decrease_score(self, amount=1):
        if self.score > 0:
            self.score -= amount
        else:
            pass

    def reset_score(self):
        self.score = 0

    def _score_text_prep(self):
        # FIXME: current_highscore should stay at the max score has ever been
        if self.score > self.leaderboard.current_highscore:
            current_highscore = self.score
        else:
            current_highscore = self.leaderboard.current_highscore

        s_text = self.font.render(f"Score: {str(self.score)} Level: {str(self.level)} "
                                  f"Highscore: {str(current_highscore)}",
                                  True, self.color)
        s_text_rect = s_text.get_rect()
        s_text_location = self.SCORE_TEXT_LOCATION_TUPLE
        return s_text, s_text_rect, s_text_location

    def _life_img_prep(self):
        life_img_location = self.LIFE_IMAGE_LOCATION_TUPLE
        life_img_rect = self.player_lives_image.get_rect()
        life_text = self.font.render("Lives Remaining: ", True, self.color)
        life_text_rect = life_text.get_rect()
        life_text_location = self.LIFE_TEXT_LOCATION_TUPLE

        life_img_rect.x, life_img_rect.y = life_img_location
        life_text_rect.x, life_text_rect.y = life_text_location
        return life_text, life_text_rect, life_text_location, life_img_rect, life_img_location

    def _powerup_img_prep(self):
        first_powerup_img_location = self.FIRST_POWERUP_LOCATION_TUPLE
        powerup_img_rect = self.super_bullet_image.get_rect()
        powerup_text = self.font.render("PowerUps: ", True, self.color)
        powerup_text_rect = powerup_text.get_rect()
        powerup_text_location = self.POWERUP_TITLE_TEXT_LOCATION_TUPLE

        powerup_img_rect.x, powerup_img_rect.y = first_powerup_img_location
        powerup_text_rect.x, powerup_text_rect.y = powerup_text_location

        return powerup_text, powerup_text_rect, powerup_text_location, powerup_img_rect, first_powerup_img_location

    def _render_extra_lives(self, screen, life_img_rect):
        for x in range(1, self.player.player_lives + 1):
            if x != 1:
                screen.blit(self.player_lives_image,
                            ((life_img_rect.x + (self.player_lives_image.get_width() * x)),
                             (life_img_rect.y + 15)))
            else:
                screen.blit(self.player_lives_image,
                            ((life_img_rect.x + (self.player_lives_image.get_width() * x)),
                             (life_img_rect.y + 15)))

    def _render_powerups(self, screen, powerup_img_rect):
        def _bilt_powerup(image, position):
            screen.blit(image, position)
        # TODO: add in if alt pressed HID keypress logic for unlimited_bullets
        for index, powerup in enumerate(self.persistent_powerups_available, start=1):
            if powerup.__class__.__name__ == 'SuperBullet':
                pu_img = self.super_bullet_image
            elif powerup.__class__.__name__ == 'UnlimitedBulletsPowerUp':
                pu_img = self.unlimited_bullets_image
            position = (powerup_img_rect.x + (int(pu_img.get_width()) * index),
                        powerup_img_rect.y + 15)
            _bilt_powerup(pu_img, position)
            # else:
            # screen.blit(self.super_bullet_image,
            #             ((powerup_img_rect.x + (self.super_bullet_image.get_width() * index)),
            #              (powerup_img_rect.y + 15)))

    def display(self, screen):
        score_text, score_text_rect, score_text_location = self._score_text_prep()
        life_text, life_text_rect, life_text_location, life_img_rect, life_img_location = self._life_img_prep()
        (powerup_text, powerup_text_rect, powerup_text_location,
         powerup_sprite_img_rect, powerup_sprite_img_location) = self._powerup_img_prep()

        # render
        self._render_extra_lives(screen, life_img_rect)
        self._render_powerups(screen, powerup_sprite_img_rect)
        # render everything else
        screen.blit(score_text, score_text_rect)
        screen.blit(life_text, life_text_rect)
        screen.blit(powerup_text, powerup_text_rect)


class FPSMon:
    """
    This module contains the `FPSMon` class, which is responsible for displaying the frames per second (FPS) on the game screen.

    Classes:
        - FPSMon

    Methods:
        - __init__(self, gs_game)
        - render_fps(self, screen)

    Attributes:
        - settings: The game's settings object.
        - clock: The game's clock object.
        - font: The font to be used for rendering the FPS.
        - color: The color of the FPS text.

    """
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.clock = gs_game.clock
        self.font = font.SysFont(self.settings.scoreboard_font_name, self.settings.scoreboard_font_size)
        self.color = self.settings.fps_counter_color

    def render_fps(self, screen):
        fps = round(self.clock.get_fps(), 2)
        fps_text = self.font.render("FPS: " + str(fps), True, self.color)
        rect = fps_text.get_rect()
        location = (1, 35)
        rect.x, rect.y = location
        screen.blit(fps_text, rect)

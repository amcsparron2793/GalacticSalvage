from pathlib import Path

from pygame.sprite import Sprite
from pygame import image, transform, font
from random import randint

class _BasePowerUpClass(Sprite):
    """
    This module contains the implementation of the `_BasePowerUpClass` class,
    which is a base class for power-up sprites in the game.

    Classes:
        - `_BasePowerUpClass`

    Attributes:
        - `SPRITE_IMAGE_PATH`: Path to the image file of the power-up sprite. (Type: `Path`)
        - `SCALE_FACTOR`: The scale factor to apply to the power-up sprite. (Type: `float`)
        - `POWERUP_TEXT`: The text to display alongside the power-up sprite. (Type: `str`)

    Methods:
        - `__init__(self, gs_game)`: Initializes a new instance of the `_BasePowerUpClass` class.
        - `_set_img_rect_and_speed(self)`: Sets the image rectangle and speed for the power-up sprite.
        - `_load_img_scale_and_rotate(self)`: Loads, scales, and rotates the power-up sprite image.
        - `update(self)`: Updates the location of the power-up sprite.
        - `draw(self, screen)`: Draws the power-up sprite on the screen.
        - `_render_and_draw_text(self, screen)`: Renders and draws the text alongside the power-up sprite.
    """
    SPRITE_IMAGE_PATH:Path = None
    SCALE_FACTOR:float = 1.0
    POWERUP_TEXT = None

    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.player = gs_game.player
        self.image = self._load_img_scale_and_rotate()
        self._set_img_rect_and_speed()

        # noinspection PyTypeChecker
        self.text:str = self.POWERUP_TEXT
        self.font = font.Font(None, 24)

    def _set_img_rect_and_speed(self):
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = randint(1, 8)

    def _load_img_scale_and_rotate(self):
        return transform.rotate(
            transform.scale_by(
                image.load(self.SPRITE_IMAGE_PATH).convert_alpha(),
                self.SCALE_FACTOR,
            ), randint(1, 360)
        )

    def update(self):
        # update LOCATION
        self.rect.y += self.speed

    def draw(self, screen):
        # Draw the sprite
        screen.blit(self.image, self.rect)
        if self.POWERUP_TEXT:
            self._render_and_draw_text(screen)

    def _render_and_draw_text(self, screen):
        # Render and draw the text
        text_surface = self.font.render(self.text, True, self.settings.WHITE)  # Render text in white
        text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))  # Position below the ship
        screen.blit(text_surface, text_rect)


class ExtraLife(_BasePowerUpClass):
    """
    The `ExtraLife` class is a subclass of `_BasePowerUpClass` and represents a power-up that gives the player an extra life.

    Attributes:
        EXTRALIFE_IMAGE_PATH (Path): The path to the image file for the extra life power-up.
        SPRITE_IMAGE_PATH (Path): The path to the image file for the sprite.
        SCALE_FACTOR (float): The scaling factor for the sprite image.

    """

    EXTRALIFE_IMAGE_PATH = Path('../Misc_Project_Files/images/1UP.png')
    SPRITE_IMAGE_PATH = EXTRALIFE_IMAGE_PATH
    SCALE_FACTOR:float = 0.15


class BrokenShip(_BasePowerUpClass):
    """
    This module contains the code for the BrokenShip class, a subclass of the _BasePowerUpClass.

    Attributes:
        BROKENSHIP_IMAGE_PATH (Path): The path to the image file for the BrokenShip sprite.
        SPRITE_IMAGE_PATH (Path): The path to the image file for the BrokenShip sprite.
        SCALE_FACTOR (float): The scale factor for the BrokenShip sprite.
        POWERUP_TEXT (str): The text displayed when the BrokenShip power-up is activated.

    Classes:
        BrokenShip (_BasePowerUpClass): A class representing a broken ship power-up.

    """

    BROKENSHIP_IMAGE_PATH = Path('../Misc_Project_Files/images/OtherShip.png')
    SPRITE_IMAGE_PATH = BROKENSHIP_IMAGE_PATH
    SCALE_FACTOR:float = 0.05
    POWERUP_TEXT = "Repair needed! Catch me!"


class SuperBulletPowerUp(_BasePowerUpClass):
    """
    This module contains the `SuperBulletPowerUp` class which is a subclass of the `_BasePowerUpClass`.

        class SuperBulletPowerUp(_BasePowerUpClass):

    Attributes:
        SUPERBULLET_IMAGE_PATH (Path): The path to the image file for the super bullet power-up.
        SPRITE_IMAGE_PATH (Path): The path to the image file used for the sprite.
        POWERUP_TEXT (str): The text that represents the super bullet power-up.

    """
    SUPERBULLET_IMAGE_PATH = Path('../Misc_Project_Files/images/SuperBullet.png')
    SPRITE_IMAGE_PATH = SUPERBULLET_IMAGE_PATH
    POWERUP_TEXT = "SUPER BULLET!"

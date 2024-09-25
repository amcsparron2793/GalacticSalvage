from pygame import Surface, SRCALPHA, draw, transform, Rect, image, time, display
from pygame.sprite import Sprite
import random

from pathlib import Path

class Asteroid(Sprite):
    """
         class Asteroid(Sprite):
    This class represents an asteroid object in the game.

    Attributes:
    - settings (Settings): The game settings object.
    - width (int): The width of the asteroid.
    - height (int): The height of the asteroid.
    - color (Tuple[int, int, int]): The color of the asteroid.
    - image (Surface): The image of the asteroid.
    - rect (Rect): The rectangular area occupied by the asteroid on the screen.
    - speed_min (int): The minimum speed of the asteroid.
    - speed_max (int): The maximum speed of the asteroid.
    - speed (int): The current speed of the asteroid.
    - angle (float): The current angle of the asteroid.
    - rotation_speed (float): The rotation speed of the asteroid.

    Methods:
    - __init__(gs_game): Initializes a new instance of the Asteroid class.
    - update(): Updates the position and rotation of the asteroid.

    __init__(self, gs_game)
    - Initializes a new instance of the Asteroid class.
    - Parameters:
      - gs_game (Game): The game instance.
    - This method initializes the attributes of the asteroid, such as its size, color, image, speed, and rotation speed.
        It also sets the initial position of the asteroid above the screen.

    update(self)
    - Updates the position and rotation of the asteroid.
    - This method updates the position of the asteroid by incrementing its y-coordinate with the current speed.
        It also updates the rotation angle of the asteroid based on the rotation speed.
    """

    ASTEROID_IMAGE_PATH = Path('../Misc_Project_Files/images/SingleAsteroid.png')
    EXPLOSION_FRAME_DIR_PATH = Path('../Misc_Project_Files/images/ExplosionPNG/')

    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        if not self.ASTEROID_IMAGE_PATH.is_file():
            self.image = Surface((self.width, self.height), SRCALPHA)
            draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        else:
            self.image = image.load(self.ASTEROID_IMAGE_PATH)
            self.image = transform.scale_by(self.image, random.uniform(
                self.settings.asteroid_scale_min, self.settings.asteroid_scale_max))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen

        self.speed_min = self.settings.asteroid_speed_min
        self.speed_max = self.settings.asteroid_speed_max * gs_game.level // 2
        if self.speed_min < 1:
            self.speed_min = 1
        if self.speed_max < 1:
            self.speed_max = 1
        # overall speed ceiling
        if not self.settings.ignore_speed_cap:
            if self.speed_max >= self.settings.asteroid_speed_cap:
                self.speed_max = self.settings.asteroid_speed_cap

        self.speed = random.randint(self.speed_min, self.speed_max)
        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1)  # Random rotation speed

    def update(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed

        # Limit the rotation angle within a range (-180 to 180 degrees)
        # if self.angle > 180:
        #     self.angle -= 360
        # elif self.angle < -180:
        #     self.angle += 360
        #
        # self.image = transform.rotate(self.image, self.angle)


class Explosion(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.animation_frames = [image.load(self.EXPLOSION_FRAME_DIR.joinpath(x)) for x in self.EXPLOSION_FRAME_DIR_PATH.iterdir()]

    def play_animation(self):
        # frame_duration = 50  # Duration of each frame in milliseconds
        for frame in self.animation_frames:
            rect = frame.get_rect()
            display.update(rect)
            self.settings.screen.blit(transform.scale_by(frame, 1.5), (rect.x, rect.y))  # Display the current frame
            # time.wait(frame_duration)  # Pause for the frame duration

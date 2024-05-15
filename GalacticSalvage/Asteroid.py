from os.path import isfile

from pygame import Surface, SRCALPHA, draw, transform, Rect, image
import random
from pygame.sprite import Sprite


class Asteroid(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        if not isfile('../Misc_Project_Files/images/SingleAsteroid.png'):
            self.image = Surface((self.width, self.height), SRCALPHA)
            draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        else:
            self.image = image.load('../Misc_Project_Files/images/SingleAsteroid.png')
            self.image = transform.scale_by(self.image, random.uniform(
                self.settings.asteroid_scale_min, self.settings.asteroid_scale_max))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen

        # FIXME: this speeds up too fast...
        self.speed_min = self.settings.asteroid_speed_min * gs_game.level // 2
        self.speed_max = self.settings.asteroid_speed_max * gs_game.level // 2
        if self.speed_min < 1:
            self.speed_min = 1
        if self.speed_max < 1:
            self.speed_max = 1

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

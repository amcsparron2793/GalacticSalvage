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
            self.image = transform.scale_by(self.image, 0.05)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = random.randint(self.settings.asteroid_speed_min, self.settings.asteroid_speed_max)
        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1)  # Random rotation speed

    def update(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed
        # self.image = transform.rotate(self.image, self.angle)
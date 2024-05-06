from pygame import Surface, SRCALPHA, draw, transform, Rect
import random
from pygame.sprite import Sprite


class Asteroid(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.color = (150, 150, 150)
        self.image = Surface((self.width, self.height), SRCALPHA)
        draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.width)
        self.rect.y = -self.settings.screen_height  # Start above the screen
        self.speed = random.randint(1, 3)
        self.angle = 0
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Random rotation speed

    def update(self):
        self.rect.y += self.speed / 2
        self.angle += self.rotation_speed
        # print(self.rect.y)
        #self.image = transform.rotate(self.image, self.angle)

    def draw_asteroid(self):
        draw.rect(self.settings.screen, self.color, self.rect)
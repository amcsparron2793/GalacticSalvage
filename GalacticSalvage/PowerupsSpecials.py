from pygame.sprite import Sprite
from pygame import image, transform
from random import randint, uniform


class BrokenShip(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.image = self._load_img_scale_and_rotate('../Misc_Project_Files/images/OtherShip.png')
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = randint(1, 8)

    # TODO: add this to other classes?
    def _load_img_scale_and_rotate(self, img_path):
        self.image = image.load(img_path)
        self.image = transform.scale_by(self.image, 0.05)
        self.image = transform.rotate(self.image, randint(1, 360))  # the ships are randomly rotated
        return self.image

    def update(self):
        self.rect.y += self.speed


from typing import Tuple
from pygame import image, Rect, draw, transform
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, gs_game):
        """ Game should be an instance of the GalacticSalvage class """
        super().__init__()
        self.settings = gs_game.settings
        self.screen = self.settings.screen
        self.color = self.settings.RED
        self.rect = Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = gs_game.player.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet up the screen. """
        # update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        draw.rect(self.screen, self.color, self.rect)


class Player(Sprite):
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.screen = self.settings.screen
        self.screen_rect = self.screen.get_rect()
        self.image = image.load('../Misc_Project_Files/images/PlayerShipNoBackground.png')
        self.image = transform.scale_by(self.image, 0.15)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.width = 50
        self.height = 50

        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ships position based on the movement flag. """
        # updates the ships x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def biltme(self):
        """ Draw the ship at its current location. """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def move_left(self):
        if self.x > 0:
            self.x -= self.settings.ship_speed

    def move_right(self):
        if self.x < self.settings.screen_width - self.width:
            self.x += self.settings.ship_speed

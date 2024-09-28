from pygame import Rect, draw
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    This documentation provides a description of the code for the Bullet class.

        class Bullet(Sprite):

    This class represents a bullet in a game. It inherits from the Sprite class.

        def __init__(self, gs_game):

    The constructor method for the Bullet class. It takes an instance of the GalacticSalvage class as a parameter.

            super().__init__()

            self.settings = gs_game.settings
            self.screen = self.settings.screen
            self.color = self.settings.bullet_color
            self.rect = Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
            self.rect.midtop = gs_game.player.rect.midtop
            self.y = float(self.rect.y)

    This method initializes the bullet. It sets the settings, screen, color, and rectangle attributes. It also sets the initial position of the bullet.

        def update(self):

    This method updates the position of the bullet.

            self.y -= self.settings.bullet_speed
            self.rect.y = self.y

    It decreases the y-coordinate of the bullet by the bullet speed specified in the game settings. It then updates the y-coordinate of the rectangle.

        def draw_bullet(self):

    This method draws the bullet on the screen.

            draw.rect(self.screen, self.color, self.rect)

    It uses the pygame draw.rect() function to draw the rectangle representing the bullet on the screen.
    """
    def __init__(self, gs_game):
        """ Game should be an instance of the GalacticSalvage class """
        super().__init__()
        self.settings = gs_game.settings
        self.screen = self.settings.screen
        self.color = self.settings.bullet_color
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

class SuperBullet(Bullet):
    def __init__(self, gs_game):
        super().__init__(gs_game)
        self.rect = Rect(0, 0, self.settings.bullet_width * self.settings.screen_width, self.settings.bullet_height)
        self.rect.midtop = gs_game.player.rect.midtop
        self.y = float(self.rect.y)
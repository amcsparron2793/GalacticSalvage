import random
from pygame import draw


class Star:
    """
    This module contains the implementation of the Star class.

    Class:
        Star:
            Represents a star in a game.

    Methods:
        __init__(self, gs_game)
            Initializes a new instance of the Star class.

        draw(self)
            Draws the star on the game screen.

        fall(self)
            Moves the star down the screen.

        OffscreenReset(self)
            Resets the star's position if it goes off the screen.

    Attributes:
        settings
            An instance of the Settings class that holds the game settings.

        color
            The color of the star.

        radius
            The radius of the star.

        x
            The x-coordinate of the star's position.

        y
            The y-coordinate of the star's position.

        yspeed
            The vertical speed at which the star falls.
    """
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.color = self.settings.WHITE
        self.radius = 1
        # why does this need to be // 15+ to fill the whole screen?
        self.x = random.randint(0, self.settings.screen_width)
        self.y = -self.settings.screen_height  # Start above the screen
        self.yspeed = random.randint(1, 3)

    def draw(self):
        draw.circle(self.settings.screen, self.color, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def OffscreenReset(self):
        if self.y >= self.settings.screen_height:
            self.y = 0
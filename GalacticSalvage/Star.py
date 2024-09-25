import random
from pygame import draw


class Star:
    """
    Represents a star in a game.

    Attributes:
        settings (object): An instance of the Settings class that holds the game settings.
        color (tuple): The color of the star.
        radius (int): The radius of the star.
        x (int): The x-coordinate of the star's position.
        y (int): The y-coordinate of the star's position.
        yspeed (int): The vertical speed at which the star falls.

    Methods:
        __init__(self, gs_game)
            Initializes a new instance of the Star class.
        draw(self)
            Draws the star on the game screen.
        fall(self)
            Moves the star down the screen.
        reset_offscreen(self)
            Resets the star's position if it goes off the screen.
    """

    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.color = self.settings.WHITE
        self.radius = 1
        self.x = random.randint(0, self.settings.screen_width)
        self.y = -self.settings.screen_height  # Start above the screen
        self.yspeed = random.randint(1, 3)

    def draw(self):
        """Draws the star on the game screen."""
        draw.circle(self.settings.screen, self.color, (self.x, self.y), self.radius)

    def fall(self):
        """Moves the star down the screen."""
        self.y += self.yspeed

    def reset_offscreen(self):
        """Resets the star's position if it goes off the screen."""
        if self.y >= self.settings.screen_height:
            self.y = -self.settings.screen_height
            self.x = random.randint(0, self.settings.screen_width)
            self.yspeed = random.randint(1, 10)
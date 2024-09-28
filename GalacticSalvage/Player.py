from pathlib import Path

from pygame import image, Rect, draw, transform
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


class Player(Sprite):
    """
    This class represents a player sprite in a game.

    The Player class extends the Sprite class.

    Attributes:
        settings (Settings): The game settings.
        screen (Surface): The game screen surface.
        screen_rect (Rect): The rect object representing the screen.
        image (Surface): The image of the player ship.
        rect (Rect): The rect object representing the player ship.
        player_lives (int): The number of lives the player has.
        width (int): The width of the player ship.
        height (int): The height of the player ship.
        x (float): The x-coordinate of the player ship.
        moving_right (bool): A flag indicating if the player is moving right.
        moving_left (bool): A flag indicating if the player is moving left.

    Methods:
        __init__(self, gs_game): Initializes a new instance of the Player class.
        update(self): Updates the position of the player ship based on the movement flags.
        blitme(self): Draws the player ship at its current location.
        center_ship(self): Centers the player ship on the screen.
        move_left(self): Moves the player ship to the left.
        move_right(self): Moves the player ship to the right.
    """
    PLAYER_IMAGE_PATH = Path('../Misc_Project_Files/images/PlayerShipNoBackground.png')
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.screen = self.settings.screen
        self.screen_rect = self.screen.get_rect()
        self.image = image.load(self.PLAYER_IMAGE_PATH)
        self.image = transform.scale_by(self.image, 0.15)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.player_lives = self.settings.starting_lives

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

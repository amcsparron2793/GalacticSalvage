from pygame.sprite import Sprite
from pygame import image, transform, font
from random import randint


class ExtraLife(Sprite):
    """
    This is the documentation for the ExtraLife class.

    class ExtraLife(Sprite):
        def __init__(self, gs_game):
            Initializes a new instance of the ExtraLife class.

            Parameters:
            - gs_game (object): An instance of the GameSettings class.

        @staticmethod
        def _load_img_scale_and_rotate(img_path):
            Loads an image from the given path, scales and rotates it.

            Parameters:
            - img_path (str): The path to the image file.

            Returns:
            - image_surface (Surface): The scaled and rotated image.

        def update(self):
            Updates the location of the ExtraLife object.

        Parameters: None

        def draw(self, screen):
            Draws the ExtraLife object on the screen.

            Parameters:
            - screen (Surface): The screen surface to draw on.
    """
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.player = gs_game.player
        self.image = self._load_img_scale_and_rotate('../Misc_Project_Files/images/1UP.png')
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = randint(1, 8)

    @staticmethod
    def _load_img_scale_and_rotate(img_path):
        image_surface = image.load(img_path).convert_alpha()
        scaled_image = transform.scale_by(image_surface, 0.15)
        rotated_image = transform.rotate(scaled_image, randint(1, 360))  # the 1UPs are randomly rotated
        return rotated_image

    def update(self):
        # update LOCATION
        self.rect.y += self.speed

    def draw(self, screen):
        # Draw the life
        screen.blit(self.image, self.rect)


class BrokenShip(Sprite):
    """
        This class represents a broken ship in a game. It is a subclass of the `Sprite` class.

        Attributes:
            settings (Settings): An instance of the `Settings` class that stores game settings.
            image (Surface): The image of the broken ship.
            rect (Rect): The rectangular area occupied by the broken ship.
            speed (int): The speed at which the broken ship moves.
            text (str): The text to be displayed alongside the broken ship.
            font (Font): The font used to render the text.

        Methods:
            __init__(self, gs_game): Initializes a new instance of the `BrokenShip` class.
            _load_img_scale_and_rotate(img_path): Loads, scales, and rotates the image of the broken ship.
            update(self): Updates the location of the broken ship.
            draw(self, screen): Draws the broken ship on the screen along with the associated text.

    """
    def __init__(self, gs_game):
        super().__init__()
        self.settings = gs_game.settings
        self.image = self._load_img_scale_and_rotate('../Misc_Project_Files/images/OtherShip.png')
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.settings.screen_height - self.rect.height  # Start above the screen
        self.speed = randint(1, 8)

        self.text = "Repair needed! Catch me!"
        self.font = font.Font(None, 24)  # Use a default font with size 24

    @staticmethod
    def _load_img_scale_and_rotate(img_path):
        image_surface = image.load(img_path).convert_alpha()
        scaled_image = transform.scale_by(image_surface, 0.05)
        rotated_image = transform.rotate(scaled_image, randint(1, 360))  # the ships are randomly rotated
        return rotated_image

    def update(self):
        # update LOCATION
        self.rect.y += self.speed

    def draw(self, screen):
        # Draw the ship
        screen.blit(self.image, self.rect)

        # Render and draw the text
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Render text in white
        text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))  # Position below the ship
        screen.blit(text_surface, text_rect)

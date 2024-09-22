from pygame import font, Rect
from GalacticSalvage.utils import ColorConverter


class Button:
    """
    This module defines a Button class that can be used to create buttons in a graphical user interface (GUI).

    Class Button:
        This class represents a button in the GUI.

        __init__(self, gs_game, msg, **kwargs):
            Initializes the Button object with the given parameters.

            - gs_game: The GameSettings object that contains the screen settings.
            - msg: The text message to be displayed on the button.
            - kwargs: Additional keyword arguments to customize the button appearance.

            If kwargs is provided, the following keyword arguments can be used:
            - width: The width of the button.
            - height: The height of the button.
            - button_color_hex: The hexadecimal color code for the button color.
            - text_color_hex: The hexadecimal color code for the text color.
            - font_name: The name of the font to be used for the button text.
            - font_size: The size of the font to be used for the button text.

        _prep_msg(self, msg):
            Turn the given message into a rendered image and center the text on the button.

            - msg: The text message to be rendered.

        draw_button(self):
            Draw the button on the screen.

            The button is drawn as a filled rectangle with the specified color, and the text message
            is displayed on top of the button.
    """
    def __init__(self, gs_game, msg, **kwargs):
        """ Init button attributes. """
        self.screen = gs_game.settings.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        font_name = None
        font_size = None
        self.font = font.SysFont(None, 48)

        if kwargs:
            if 'width' in kwargs:
                self.width = kwargs['width']
            if 'height' in kwargs:
                self.height = kwargs['height']
            if 'button_color_hex' in kwargs:
                self.button_color = ColorConverter.hex_to_rgb(kwargs['button_color_hex'])
            if 'text_color_hex' in kwargs:
                self.text_color = ColorConverter.hex_to_rgb(kwargs['text_color_hex'])
            if 'font_name' in kwargs:
                font_name = kwargs['font_name']
            if 'font_size' in kwargs:
                font_size = kwargs['font_size']
            if font_name and font_size:
                self.font = font.SysFont(font_name, font_size)

        # build the buttons rect object and center it
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # the button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """ Turn msg into a rendered image and center text on the button. """

        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # draw the blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

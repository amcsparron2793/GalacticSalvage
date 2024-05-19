from pygame import font, Rect
from utils import ColorConverter


class Button:
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

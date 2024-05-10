from pygame import display
from GsConfig import GsConfig


class Settings:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Colors
    def __init__(self, **kwargs):
        self.config = GsConfig('config.ini', '../cfg')
        self.config.GetConfig()

        if 'use_fullscreen' in kwargs:
            self.use_fullscreen = kwargs['use_fullscreen']
        else:
            windowed = self.config.getboolean('DEFAULT', 'windowed_mode')
            if windowed:
                self.use_fullscreen = False
            else:
                self.use_fullscreen = True

        # Set up the screen dimensions
        self.screen_width = self.config.getint('DEFAULT', 'screen_width')
        self.screen_height = self.config.getint('DEFAULT', 'screen_height')
        self.fullscreen_width_height = display.get_desktop_sizes()

        if not self.use_fullscreen:
            self.screen = display.set_mode((self.config.getint('DEFAULT', 'screen_width'),
                                            self.config.getint('DEFAULT', 'screen_height')))
        else:
            self.screen = display.set_mode(self.fullscreen_width_height[0])

        display.set_caption("Galactic Salvage")
        self.bg_color = self.BLACK

        self.bullet_width = self.config.getint('BULLET', 'bullet_width')
        self.bullet_height = self.config.getint('BULLET', 'bullet_height')
        self.bullet_color = self.RED

        self.bullet_speed = self.config.getint('BULLET', 'bullet_speed')
        self.bullets_allowed = self.config.getint('BULLET', 'bullets_allowed')

        self.ship_speed = 5

        self.asteroid_speed_min = self.config.getint('ASTEROID', 'asteroid_speed_min')
        self.asteroid_speed_max = self.config.getint('ASTEROID', 'asteroid_speed_max')

        self.scoreboard_font_name = self.config.get('SCOREBOARD', 'font_name')
        self.scoreboard_font_size = self.config.getint('SCOREBOARD', 'font_size')
        self.scoreboard_font_color = self.WHITE

        self.sound_muted = self.config.getboolean('DEFAULT', 'sound_muted')

    @staticmethod
    def ToggleFullscreen():
        display.toggle_fullscreen()


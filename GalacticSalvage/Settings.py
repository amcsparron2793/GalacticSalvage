from pygame import display
from GalacticSalvage.GsConfig import GsConfig
from GalacticSalvage.utils import ColorConverter


class Settings:
    """
    This class represents the settings for the game.

    Attributes:
        BLACK: A tuple representing the RGB value for black color.
        WHITE: A tuple representing the RGB value for white color.
        RED: A tuple representing the RGB value for red color.
        config: An instance of GsConfig class which is used to get the game configuration.
        use_fullscreen: A boolean indicating whether to use fullscreen mode or not.
        screen_width: An integer representing the width of the game screen.
        screen_height: An integer representing the height of the game screen.
        fullscreen_width_height: A tuple representing the width and height of the screen in fullscreen mode.
        screen: An instance of the display set to the desired mode.
        bg_color: A tuple representing the RGB value for the background color.
        bullet_width: An integer representing the width of the bullet.
        bullet_height: An integer representing the height of the bullet.
        bullet_color: A tuple representing the RGB value for the bullet color.
        bullet_speed: An integer representing the speed of the bullet.
        bullets_allowed: An integer representing the maximum number of bullets allowed on the screen.
        ship_speed: An integer representing the speed of the ship.
        starting_lives: An integer representing the number of lives the player starts with.
        asteroid_speed_min: An integer representing the minimum speed of an asteroid.
        asteroid_speed_max: An integer representing the maximum speed of an asteroid.
        asteroid_scale_min: A float representing the minimum scale of an asteroid.
        asteroid_scale_max: A float representing the maximum scale of an asteroid.
        asteroid_speed_cap: An integer representing the maximum speed of asteroids.
        ignore_speed_cap: A boolean indicating whether to ignore the speed cap for asteroids or not.
        scoreboard_font_name: A string representing the name of the font used for the scoreboard.
        scoreboard_font_size: An integer representing the size of the font used for the scoreboard.
        scoreboard_font_color: A tuple representing the RGB value for the font color used in the scoreboard.
        fps_counter_color: A tuple representing the RGB value for the color of the FPS counter.
        show_fps: A boolean indicating whether to show the FPS counter or not.
        sound_muted: A boolean indicating whether the sound is muted or not.

    Methods:
        __init__(self, **kwargs):
            Initializes the Settings object with the given keyword arguments.
        ToggleFullscreen():
            Toggles the fullscreen mode of the display.
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

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

        self.bg_color = ColorConverter.hex_to_rgb(self.config.get('DEFAULT', 'bg_color'))

        self.bullet_width = self.config.getint('BULLET', 'bullet_width')
        self.bullet_height = self.config.getint('BULLET', 'bullet_height')
        self.bullet_color = ColorConverter.hex_to_rgb(self.config.get('BULLET', 'bullet_color'))

        self.bullet_speed = self.config.getint('BULLET', 'bullet_speed')
        self.bullets_allowed = self.config.getint('BULLET', 'bullets_allowed')

        self.ship_speed = 5
        self.starting_lives = self.config.getint('PLAYER', 'starting_lives')

        self.asteroid_speed_min = self.config.getint('ASTEROID', 'asteroid_speed_min')
        self.asteroid_speed_max = self.config.getint('ASTEROID', 'asteroid_speed_max')
        self.asteroid_scale_min = self.config.getfloat('ASTEROID', 'asteroid_scale_min')
        self.asteroid_scale_max = self.config.getfloat('ASTEROID', 'asteroid_scale_max')
        self.asteroid_speed_cap = self.config.getint('ASTEROID', 'asteroid_speed_cap')
        self.ignore_speed_cap = self.config.getboolean('ASTEROID', 'ignore_speed_cap')

        self.scoreboard_font_name = self.config.get('SCOREBOARD', 'font_name')
        self.scoreboard_font_size = self.config.getint('SCOREBOARD', 'font_size')
        self.scoreboard_font_color = ColorConverter.hex_to_rgb(
            self.config.get('SCOREBOARD', 'scoreboard_font_color'))
        self.fps_counter_color = ColorConverter.hex_to_rgb(
            self.config.get('SCOREBOARD', 'fps_counter_color'))
        self.show_fps = self.config.getboolean('DEFAULT', 'show_fps')

        self.sound_muted = self.config.getboolean('DEFAULT', 'sound_muted')

    @staticmethod
    def ToggleFullscreen():
        display.toggle_fullscreen()


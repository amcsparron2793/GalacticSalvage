from pygame import display

try:
    from .GsConfig import GsConfig
    from .utils import ColorConverter
except ImportError:
    from GsConfig import GsConfig
    from utils import ColorConverter


class Settings:
    """
    This module defines a `Settings` class that stores various game settings.

    Example usage:

    ```python
    settings = Settings()
    # access and modify settings
    settings.ship_speed = 10
    ```

    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self, **kwargs):
        self.config = GsConfig('config.ini', '../cfg')
        self.config.GetConfig()

        self._setup_screen(kwargs.get('use_fullscreen',
                                      not self.config.getboolean('DEFAULT', 'windowed_mode')))
        self._init_player_settings()
        self._init_bullet_settings()
        self._init_asteroid_settings()
        self._init_scoreboard_settings()
        self._init_sound_settings()

        self.leaderboard_db_location = self.config.get('LEADERBOARD', 'database_file_path')

    def _setup_screen(self, use_fullscreen):
        self.show_fps = self.config.getboolean('DEFAULT', 'show_fps')
        self.bg_color = ColorConverter.hex_to_rgb(self.config.get('DEFAULT', 'bg_color'))
        self.use_fullscreen = use_fullscreen
        self.screen_width = self.config.getint('DEFAULT', 'screen_width')
        self.screen_height = self.config.getint('DEFAULT', 'screen_height')
        screen_size = (self.screen_width, self.screen_height)

        display.set_caption("Galactic Salvage")

        if self.use_fullscreen:
            info = display.Info()
            screen_size = (info.current_w, info.current_h)
        self.screen = display.set_mode(screen_size)

    def _init_player_settings(self):
        self.ship_speed = 5
        self.starting_lives = self.config.getint('PLAYER', 'starting_lives')

    def _init_sound_settings(self):
        self.sfx_volume = self.config.getfloat('DEFAULT', 'sfx_volume') / 100
        self.music_volume = self.config.getfloat('DEFAULT', 'music_volume') / 100
        self.sound_muted = self.config.getboolean('DEFAULT', 'sound_muted')

    def _init_bullet_settings(self):
        self.bullet_width = self.config.getint('BULLET', 'bullet_width')
        self.bullet_height = self.config.getint('BULLET', 'bullet_height')
        self.bullet_color = ColorConverter.hex_to_rgb(self.config.get('BULLET', 'bullet_color'))
        self.bullet_speed = self.config.getint('BULLET', 'bullet_speed')
        self.bullets_allowed = self.config.getint('BULLET', 'bullets_allowed')

    def _init_asteroid_settings(self):
        self.asteroid_speed_min = self.config.getint('ASTEROID', 'asteroid_speed_min')
        self.asteroid_speed_max = self.config.getint('ASTEROID', 'asteroid_speed_max')
        self.asteroid_scale_min = self.config.getfloat('ASTEROID', 'asteroid_scale_min')
        self.asteroid_scale_max = self.config.getfloat('ASTEROID', 'asteroid_scale_max')
        self.asteroid_speed_cap = self.config.getint('ASTEROID', 'asteroid_speed_cap')
        self.ignore_speed_cap = self.config.getboolean('ASTEROID', 'ignore_speed_cap')

    def _init_scoreboard_settings(self):
        self.scoreboard_font_name = self.config.get('SCOREBOARD', 'font_name')
        self.scoreboard_font_size = self.config.getint('SCOREBOARD', 'font_size')
        self.scoreboard_font_color = ColorConverter.hex_to_rgb(self.config.get('SCOREBOARD', 'scoreboard_font_color'))
        self.fps_counter_color = ColorConverter.hex_to_rgb(self.config.get('SCOREBOARD', 'fps_counter_color'))

    @staticmethod
    def toggle_fullscreen():
        display.toggle_fullscreen()

from BetterConfigAJM import BetterConfigAJM as BetterConfig
from .utils import ColorConverter


class GsConfig(BetterConfig):
    """
    Class GsConfig

    This class is a subclass of BetterConfig. It represents a game configuration object that is used to store and retrieve configuration settings for the game.

    Constructor:
        def __init__(self, config_filename, config_dir, config_list_dict=None, *args, **kwargs):
            Constructs a GsConfig object with the specified configuration file name, directory, and optional configuration list dictionary. If a configuration list dictionary is not provided, the default configuration list will be used.

    Attributes:
        config_list_dict (list): A list of dictionaries representing configuration settings for different aspects of the game.

    Methods: None

    Example usage:
        # Create a GsConfig object with default configuration
        config = GsConfig("config.ini", "/path/to/config")

        # Retrieve a configuration setting
        safe_mode = config.config_list_dict[0]['DEFAULT']['safe_mode']

    Note: The GsConfig class inherits all attributes and methods from the BetterConfig class.
    """
    def __init__(self, config_filename, config_dir, config_list_dict=None, *args, **kwargs):
        super().__init__(config_filename, config_dir, config_list_dict, *args, **kwargs)

        self.default_config = [
            {
                'DEFAULT':
                    {
                        'safe_mode': 'False',
                        'windowed_mode': 'True',
                        'screen_width': 800,
                        'screen_height': 600,
                        'sound_muted': 'False',
                        'bg_color': ColorConverter.rgb_to_hex((0, 0, 0)),
                        'show_fps': 'False'
                    },
                'PLAYER':
                    {
                        'starting_lives': 3
                    },
                'BULLET':
                    {
                        'bullet_width': 5,
                        'bullet_height': 15,
                        'bullets_allowed': 3,
                        'bullet_speed':  5,
                        'bullet_color': ColorConverter.rgb_to_hex((255, 0, 0))
                    },
                'SCOREBOARD':
                    {
                        'font_name': '',
                        'font_size': 30,
                        'scoreboard_font_color': ColorConverter.rgb_to_hex((255, 255, 255)),
                        'fps_counter_color': ColorConverter.rgb_to_hex((149, 151, 154))
                    },
                'ASTEROID':
                    {
                        'asteroid_speed_min': 2,
                        'asteroid_speed_max': 6,
                        'asteroid_total_max': 5,
                        'asteroid_scale_min': 0.02,
                        'asteroid_scale_max': 0.08,
                        'asteroid_speed_cap': 12,
                        'ignore_speed_cap': False
                    }
            }
        ]

        if config_list_dict:
            self.config_list_dict = config_list_dict
        else:
            self.config_list_dict = self.default_config

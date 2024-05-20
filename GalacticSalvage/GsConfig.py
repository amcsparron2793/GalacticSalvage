from BetterConfigAJM import BetterConfigAJM as BetterConfig
from utils import ColorConverter


class GsConfig(BetterConfig):
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
                    },
                'LEADERBOARD':
                    {
                        'database_file_path': '../Misc_Project_Files/GS_Leaderboard.db'
                    }
            }
        ]

        if config_list_dict:
            self.config_list_dict = config_list_dict
        else:
            self.config_list_dict = self.default_config

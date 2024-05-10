from BetterConfigAJM import BetterConfigAJM as BetterConfig


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
                        'sound_muted': 'False'
                    },
                'BULLET':
                    {
                        'bullet_width': 5,
                        'bullet_height': 15,
                        'bullets_allowed': 3,
                        'bullet_speed':  5
                    },
                'SCOREBOARD':
                    {
                        'font_name': '',
                        'font_size': 30,
                    },
                'ASTEROID':
                    {
                        'asteroid_speed_min': 1,
                        'asteroid_speed_max': 3,
                        'asteroid_total_max': 5,
                        'asteroid_scale_min': 0.03,
                        'asteroid_scale_max': 0.07
                    }
            }
        ]

        if config_list_dict:
            self.config_list_dict = config_list_dict
        else:
            self.config_list_dict = self.default_config

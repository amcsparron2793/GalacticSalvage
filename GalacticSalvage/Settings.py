from pygame import display, mixer


class Sounds:
    def __init__(self):
        self.blaster = mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.player_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')
        self.missed_asteroid = mixer.Sound('../Misc_Project_Files/sounds/MissedAsteroid.mp3')
        self.asteroid_boom = mixer.Sound('../Misc_Project_Files/sounds/BoomAsteroid.mp3')


class Settings:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Colors
    def __init__(self):
        # Set up the screen dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.screen = display.set_mode((self.screen_width, self.screen_height))
        display.set_caption("Galactic Salvage")
        self.bg_color = self.BLACK

        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = self.RED
        self.bullet_speed = 5
        self.bullets_allowed = 3
        self.ship_speed = 5


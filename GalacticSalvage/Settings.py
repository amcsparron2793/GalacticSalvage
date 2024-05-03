from pygame import display, mixer


class Sounds:
    def __init__(self):
        self.blaster_sound = mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.boom_sound = mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')


class Settings:
    # Set up the screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display.set_caption("Galactic Salvage")
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

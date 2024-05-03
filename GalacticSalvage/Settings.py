from pygame import display


class Settings:
    # Set up the screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display.set_caption("Galactic Salvage")
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

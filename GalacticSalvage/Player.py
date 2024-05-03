from typing import Tuple
from pygame import mixer
from Settings import Settings


class Player:
    def __init__(self, color: Tuple[int, int, int] = (0, 255, 0), projectile_cooldown: int = 15):
        self.width = 50
        self.height = 50
        self.color = color
        self.x = Settings.SCREEN_WIDTH // 2 - self.width // 2
        self.y = Settings.SCREEN_HEIGHT - self.height - 20
        self.speed = 5
        self.projectile_cooldown = projectile_cooldown  # Cooldown period in frames
        self.cooldown_counter = 0
        self.blaster = mixer.Sound('../Misc_Project_Files/sounds/blaster.mp3')
        self.boom = mixer.Sound('../Misc_Project_Files/sounds/BoomPlayer.mp3')
        # TODO: add score var etc.

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < Settings.SCREEN_WIDTH - self.width:
            self.x += self.speed

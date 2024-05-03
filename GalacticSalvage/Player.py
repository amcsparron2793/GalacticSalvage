from typing import Tuple
from Settings import Settings


class Projectile:
    def __init__(self, x, y, color: Tuple[int, int, int] = (255, 0, 0)):
        self.width = 5
        self.height = 15
        self.color = color
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed


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

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < Settings.SCREEN_WIDTH - self.width:
            self.x += self.speed

from typing import Tuple


class Projectile:
    def __init__(self, gs_game, x, y):
        """ Game should be an instance of the GalacticSalvage class """
        self.x = x
        self.y = y
        self.settings = gs_game.settings
        self.speed = self.settings.bullet_speed

    def move(self):
        self.y -= self.speed


class Player:
    def __init__(self, gs_game, color: Tuple[int, int, int] = (0, 255, 0), projectile_cooldown: int = 15):
        self.width = 50
        self.height = 50
        self.color = color
        self.settings = gs_game.settings
        self.x = self.settings.screen_width // 2 - self.width // 2
        self.y = self.settings.screen_height - self.height - 20
        self.speed = 5
        self.projectile_cooldown = projectile_cooldown  # Cooldown period in frames
        self.cooldown_counter = 0

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < self.settings.screen_width - self.width:
            self.x += self.speed

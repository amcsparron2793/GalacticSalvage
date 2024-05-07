import random
from pygame import draw


class Star:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.color = self.settings.WHITE
        self.radius = 1
        # why does this need to be // 15+ to fill the whole screen?
        self.x = random.randint(0, self.settings.screen_width)
        self.y = -self.settings.screen_height  # Start above the screen
        self.yspeed = random.randint(1, 3)

    def draw(self):
        draw.circle(self.settings.screen, self.color, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def OffscreenReset(self):
        if self.y >= self.settings.screen_height:
            self.y = 0
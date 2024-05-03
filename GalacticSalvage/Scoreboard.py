from Settings import Settings
from pygame import font


class Scoreboard:
    def __init__(self, font_size=30):
        self.score = 0
        self.font = font.SysFont(None, font_size)
        self.color = Settings.WHITE

    def increase_score(self, amount=1):
        self.score += amount

    def decrease_score(self, amount=1):
        if self.score > 0:
            self.score -= amount
        else:
            pass

    def reset_score(self):
        self.score = 0

    def display(self, screen):
        score_text = self.font.render("Score: " + str(self.score), True, self.color)
        screen.blit(score_text, (10, 10))



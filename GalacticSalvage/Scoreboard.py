from pygame import font


class Scoreboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.score = 0
        self.font = font.SysFont(self.settings.scoreboard_font_name, self.settings.scoreboard_font_size)
        self.color = self.settings.scoreboard_font_color

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



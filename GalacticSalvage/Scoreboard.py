from pygame import font


class Scoreboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.level = gs_game.level
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
        score_text = self.font.render(f"Score: {str(self.score)} "
                                      f"Level: {str(self.level)}", True, self.color)
        rect = score_text.get_rect()
        location = (10, 10)
        rect.x, rect.y = location
        screen.blit(score_text, rect)


class FPSMon:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.clock = gs_game.clock
        self.font = font.SysFont(self.settings.scoreboard_font_name, self.settings.scoreboard_font_size)
        self.color = self.settings.fps_counter_color

    def render_fps(self, screen):
        fps = round(self.clock.get_fps(), 2)
        score_text = self.font.render("FPS: " + str(fps), True, self.color)
        rect = score_text.get_rect()
        location = (10, 35)
        rect.x, rect.y = location
        screen.blit(score_text, rect)

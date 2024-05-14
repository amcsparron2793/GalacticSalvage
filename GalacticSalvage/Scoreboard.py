from pygame import font, image, transform


class Scoreboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.score = 0
        self.font = font.SysFont(self.settings.scoreboard_font_name, self.settings.scoreboard_font_size)
        self.color = self.settings.scoreboard_font_color
        self.image = image.load('../Misc_Project_Files/images/PlayerShipNoBackground.png')
        self.image = transform.scale_by(self.image, 0.05)

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
        score_text_rect = score_text.get_rect()
        score_text_location = (10, 10)
        life_img_location = (1, 45)
        life_img_rect = self.image.get_rect()

        life_img_rect.x, life_img_rect.y = life_img_location
        # FIXME: this doesnt update when the amount of lives change.
        for x in range(1,  self.settings.starting_lives + 1):
            if x != 1:
                screen.blit(self.image, ((life_img_rect.x + (self.image.get_width() * x)), (life_img_rect.y + 15)))
            else:
                screen.blit(self.image, ((life_img_rect.x + (self.image.get_width() * x)), (life_img_rect.y + 15)))
        score_text_rect.x, score_text_rect.y = score_text_location
        screen.blit(score_text, score_text_rect)


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

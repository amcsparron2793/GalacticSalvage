from pygame import font, image, transform


class Scoreboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.level = gs_game.level
        self.player = gs_game.player
        self.score = 0
        self.font = font.SysFont(self.settings.scoreboard_font_name,
                                 self.settings.scoreboard_font_size)
        self.color = self.settings.scoreboard_font_color

        self.player_lives_image = image.load('../Misc_Project_Files/images/PlayerShipNoBackground.png')
        self.player_lives_image = transform.scale_by(self.player_lives_image, 0.05)

    def increase_score(self, amount=1):
        self.score += amount

    def decrease_score(self, amount=1):
        if self.score > 0:
            self.score -= amount
        else:
            pass

    def reset_score(self):
        self.score = 0

    def _score_text_prep(self):
        s_text = self.font.render(f"Score: {str(self.score)} Level {str(self.level)}", True, self.color)
        s_text_rect = s_text.get_rect()
        s_text_location = (10, 10)
        return s_text, s_text_rect, s_text_location

    def _life_img_prep(self):
        life_img_location = (1, 75)
        life_img_rect = self.player_lives_image.get_rect()
        life_text = self.font.render("Lives Remaining: ", True, self.color)
        life_text_rect = life_text.get_rect()
        life_text_location = (1, 65)

        life_img_rect.x, life_img_rect.y = life_img_location
        life_text_rect.x, life_text_rect.y = life_text_location
        return life_text, life_text_rect, life_text_location, life_img_rect, life_img_location

    def _render_extra_lives(self, screen, life_img_rect):
        for x in range(1, self.player.player_lives + 1):
            if x != 1:
                screen.blit(self.player_lives_image,
                            ((life_img_rect.x + (self.player_lives_image.get_width() * x)),
                             (life_img_rect.y + 15)))
            else:
                screen.blit(self.player_lives_image,
                            ((life_img_rect.x + (self.player_lives_image.get_width() * x)),
                             (life_img_rect.y + 15)))

    def display(self, screen):
        score_text, score_text_rect, score_text_location = self._score_text_prep()
        life_text, life_text_rect, life_text_location, life_img_rect, life_img_location = self._life_img_prep()

        # render
        self._render_extra_lives(screen, life_img_rect)
        # render everything else
        screen.blit(score_text, score_text_rect)
        screen.blit(life_text, life_text_rect)


class FPSMon:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.clock = gs_game.clock
        self.font = font.SysFont(self.settings.scoreboard_font_name, self.settings.scoreboard_font_size)
        self.color = self.settings.fps_counter_color

    def render_fps(self, screen):
        fps = round(self.clock.get_fps(), 2)
        fps_text = self.font.render("FPS: " + str(fps), True, self.color)
        rect = fps_text.get_rect()
        location = (1, 35)
        rect.x, rect.y = location
        screen.blit(fps_text, rect)

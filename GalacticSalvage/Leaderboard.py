from SQLLite3HelperClass import SQLlite3Helper
from pygame import Rect, font, draw
from pygame.constants import *
from typing import List


class InputBox:
    # TODO: need get player name - this is GPT generated, needs to be integrated.
    def __init__(self, x, y, w, h, font_size=74, text=''):
        self.rect = Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.text = text
        self.font = font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (200, 200, 200) if self.active else (0, 0, 0)

        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    return self.text  # Return the text when Enter is pressed
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        draw.rect(screen, self.color, self.rect, 2)


class Leaderboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.game = gs_game
        self.sql = SQLlite3Helper(self.settings.leaderboard_db_location)
        self.cxn, self.csr = self.sql.GetConnectionAndCursor()
        self._leaderboard = None
        self._top_ten_leaderboard = None
        self._current_highscore = None

    @property
    def leaderboard(self) -> List[dict]:
        q_str = f"""select * from FullLeaderboard"""
        self.sql.Query(q_str)
        self._leaderboard = self.sql.list_dict_results
        return self._leaderboard

    @property
    def top_ten_leaderboard(self):
        q_str = f"""select * 
                    from FullLeaderboard 
                    order by score desc
                    limit 10"""
        self.sql.Query(q_str)
        self._top_ten_leaderboard = self.sql.list_dict_results
        return self._top_ten_leaderboard

    @property
    def current_highscore(self) -> int:
        q_str = f"""select max(score) from Leaderboard"""
        self.sql.Query(q_str)
        self._current_highscore = self.sql.query_results[0][0]
        return self._current_highscore

    def _get_player_id(self, player_name):
        q_str = f"""select id from Players where lower(player_name) = '{player_name}' """
        self.sql.Query(q_str)
        if len(self.sql.query_results) <= 0:
            self._make_new_player(player_name)
            self._get_player_id(player_name)
        return self.sql.query_results[0][0]

    def _make_new_player(self, player_name):
        q_str = f"""insert into Players(player_name) values('{player_name}')"""
        self.sql.Query(q_str)
        self.cxn.commit()

    def add_entry(self, player_name: str):
        player_name = player_name.lower()
        score = self.game.scoreboard.score
        level = self.game.level
        player_id = self._get_player_id(player_name)
        q_str = f"""insert into Leaderboard(player_id, score, level) VALUES ({player_id}, {score}, {level})"""
        print(q_str)
        self.sql.Query(q_str)
        self.cxn.commit()

    def get_player_name(self):
        # TODO: this needs to be tweaked to work with the game - GPT generated.
        input_box = InputBox(100, 100, 140, 50)
        clock = pygame.time.Clock()
        player_name = None
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                result = input_box.handle_event(event)
                if result:
                    player_name = result
                    done = True

            input_box.update()
            self.settings.screen.fill((255, 255, 255))
            input_box.draw(self.settings.screen)

            prompt_surface = pygame.font.Font(None, 50).render('Enter your name:', True, (0, 0, 0))
            self.settings.screen.blit(prompt_surface, (100, 50))

            pygame.display.flip()
            clock.tick(30)





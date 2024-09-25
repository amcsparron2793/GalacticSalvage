try:
    from .GsDatabase import GsDatabase
except ImportError as e:
    from GsDatabase import GsDatabase
from pygame import Rect, draw, time, font, display, event as pg_event, quit as pg_quit
from pygame.constants import *
from typing import List


class InputBox:
    ACTIVE_COLOR = (255, 255, 255)
    INACTIVE_COLOR = (200, 200, 200)
    INITIAL_COLOR = (255, 255, 255)
    TEXT_COLOR = (255, 255, 255)
    WIDTH_INCREMENT = 10
    MIN_WIDTH = 200

    def __init__(self, x, y, w, h, font_size=74, text=''):
        self.rect = Rect(x, y, w, h)
        self.box_color = self.INITIAL_COLOR
        self.text = text
        self.font = font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.box_color)
        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.box_color = self.ACTIVE_COLOR if self.active else self.INACTIVE_COLOR

        if event.type == KEYDOWN and self.active:
            if event.key == K_RETURN:
                return self.text if self.text.strip() else None  # Return text when Enter is pressed, ensure it’s not empty
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.TEXT_COLOR)

    def update(self):
        width = max(self.MIN_WIDTH, self.txt_surface.get_width() + self.WIDTH_INCREMENT)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        draw.rect(screen, self.box_color, self.rect, 2)

class Leaderboard:
    BACKGROUND_COLOR = (0, 0, 0)
    INSTRUCTIONS_COLOR = (255, 255, 255)
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.sql = GsDatabase(self.settings.leaderboard_db_location)
        self.cxn, self.csr = self.sql.GetConnectionAndCursor()
        self.game = gs_game
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
                    from TopTenLeaderboard"""
        self.sql.Query(q_str)
        self._top_ten_leaderboard = self.sql.list_dict_results
        return self._top_ten_leaderboard

    @property
    def current_highscore(self) -> int:
        q_str = f"""select max(score) from Leaderboard"""
        self.sql.Query(q_str)
        self._current_highscore = self.sql.query_results[0][0] or 0
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
        player_name_input_width = 140
        player_name_input_height = 50
        center_x = self.settings.screen.get_rect().center[0]
        center_y = self.settings.screen.get_rect().center[1]
        input_box = InputBox(x=(center_x - player_name_input_width),
                             y=(center_y - player_name_input_height),
                             w=player_name_input_width, h=player_name_input_height)
        clock = time.Clock()
        player_name = None
        done = False

        p_name_font = font.Font(None, 50)

        while not done:
            for event in pg_event.get():
                if event.type == QUIT:
                    pg_quit()
                    return None
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    #done = True
                    pg_quit()
                else:
                    result = input_box.handle_event(event)
                    if result:
                        player_name = result
                        done = True

            input_box.update()

            self.settings.screen.fill(self.BACKGROUND_COLOR)#(255, 255, 255))
            input_box.draw(self.settings.screen)

            instructions_prompt_surface = p_name_font.render('Enter your name:',
                                                             True,
                                                             self.INSTRUCTIONS_COLOR)
            instructions_prompt_surface_x = center_x - player_name_input_width * 1.25
            instructions_prompt_surface_y = center_y - player_name_input_height * 2
            self.settings.screen.blit(instructions_prompt_surface, (instructions_prompt_surface_x,
                                                                    instructions_prompt_surface_y))

            display.flip()
            clock.tick(30)

        return player_name

    def get_final_leaderboard_strings(self):
        # TODO: fix the design of the scoreboard itself
        final_strings = []
        # assuming top_ten_leaderboard holds the top 10 players' names and scores
        leaderboard_info = [x.items() for x in self.top_ten_leaderboard]
        for rank, (player, date, score, level) in enumerate(leaderboard_info, start=1):
            final_string = (f"{rank}. {date[0]}: {date[1]} - {player[0]}: {player[1]} "
                            f"- {score[0]}: {score[1]} - {level[0]}: {level[1]}")
            final_strings.append(final_string)
        return final_strings

    def console_display_leaderboard(self):
        """
        Prints the leaderboard in a formatted manner.
        """
        print("Leaderboard:")
        print("----------------------------")
        for entry in self.get_final_leaderboard_strings():
            print(entry)




from SQLLite3HelperClass import SQLlite3Helper
from typing import List


class Leaderboard:
    def __init__(self, gs_game):
        self.settings = gs_game.settings
        self.game = gs_game
        self.sql = SQLlite3Helper(self.settings.leaderboard_db_location)
        self.cxn, self.csr = self.sql.GetConnectionAndCursor()
        self._leaderboard = None
        self._top_ten_leaderboard = None

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




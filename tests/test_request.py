import unittest
from datetime import date, timedelta

from game_app import app

NBA_url = "http://data.nba.net/10s/prod/v1/20211211/scoreboard.json"
#yesterday = "20211212"

# TODO: Add test for no games the previous night
# TODO: Check for catching results of multiple close games
# TODO: Check for catching no results on a day with no close games, e.g. 09 Dec 21

class TestRequests(unittest.TestCase):
    def test_check_close_game(self):

        response = app.check_close_game(NBA_url)
        self.assertEqual(response, ['ORL : LAC'])

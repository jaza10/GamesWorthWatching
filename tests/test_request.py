import unittest

from game_app import app

NBA_url = "http://data.nba.net/10s/prod/v1/20211211/scoreboard.json"

# TODO: Add test for no games the previous night
# TODO: Check for catching results of multiple close games
# TODO: Check for catching no results on a day with no close games, e.g. 09 Dec 21

class TestRequests(unittest.TestCase):
    def test_check_close_game(self):

        response = app.check_close_game(NBA_url)
        self.assertEqual(response, 'Games worth watching on 20211212: ORL : LAC, \n')
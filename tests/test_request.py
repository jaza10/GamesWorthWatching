import unittest

from game_app import app

NBA_url = "http://data.nba.net/10s/prod/v1/20211211/scoreboard.json"

class TestRequests(unittest.TestCase):
    def test_check_close_game(self):

        response = app.check_close_game(NBA_url)
        self.assertEqual(response, 'Games worth watching on 2021-12-11: ORL : LAC, \n')
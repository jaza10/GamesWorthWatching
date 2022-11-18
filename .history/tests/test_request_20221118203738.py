import unittest
import json
from datetime import date, timedelta

from game_app import app

NBA_url = "http://data.nba.net/10s/prod/v1/20211211/scoreboard.json"
#yesterday = "20211212"

# TODO: Add test for no games the previous night
# TODO: Check for catching results of multiple close games
# TODO: Check for catching no results on a day with no close games, e.g. 09 Dec 21

class TestRequests(unittest.TestCase):

        # write a test for return_results function
    def test_return_results(self):
        testJSON = open('tests/resources/todaysScoreboard_00.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.return_results(data)
        self.assertEqual(response, {'0022200223': {'vteam_name': 'DET', 'hteam_name': 'LAC', 'vteam_score': 91, 'hteam_score': 96, 'score_diff': 5, 'game_summary_url': 'https://www.nba.com/game/DET-vs-LAC-0022200223?watch'}, '0022200221': {'vteam_name': 'BKN', 'hteam_name': 'POR', 'vteam_score': 109, 'hteam_score': 107, 'score_diff': 2, 'game_summary_url': 'https://www.nba.com/game/BKN-vs-POR-0022200221?watch'}})
    
    # write a test for get_game_information function
    def test_get_game_information(self):
        testJSON = open('tests/resources/boxscore_0022200202_close.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.get_game_information(data)
        self.assertEqual(response, {'vteam_name': 'DET', 'hteam_name': 'LAC', 'vteam_score': 91, 'hteam_score': 96, 'score_diff': 5, 'game_summary_url': 'https://www.nba.com/game/DET-vs-LAC-0022200223?watch'})

    # write a test for get_game_summary_url function
    def test_get_game_summary_url(self):
        testJSON = open('tests/resources/boxscore_0022200202_close.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.get_game_summary_url(data)
        self.assertEqual(response, 'https://www.nba.com/game/DET-vs-LAC-0022200223?watch')

    # write a test for get_score_diff function
    def test_get_score_diff(self):
        testJSON = open('tests/resources/boxscore_0022200202_close.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.get_score_diff(data)
        self.assertEqual(response, 5)

    # write a test for check_if_close function
    def check_if_it_was_a_close_game(self):
        testJSON = open('tests/resources/boxscore_0022200202_close.json')
        data_close = json.load(testJSON)
        testJSON = open('tests/resources/boxscore_0022200205_not_close.json')
        data_not_close = json.load(testJSON)
        testJSON.close()
        response = app.check_if_it_was_a_close_game(data_close)
        self.assertEqual(response, True)
        response = app.check_if_it_was_a_close_game(data_not_close)
        self.assertEqual(response, False)

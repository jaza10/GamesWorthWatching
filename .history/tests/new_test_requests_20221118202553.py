import unittest
import json
from datetime import date, timedelta

from game_app import app

#NBA_url = "http://data.nba.net/10s/prod/v1/20211211/scoreboard.json"
#yesterday = "20211212"

# TODO: Add test for no games the previous night
# TODO: Check for catching results of multiple close games
# TODO: Check for catching no results on a day with no close games, e.g. 09 Dec 21

# Add completely new tests here

class TestRequests(unittest.TestCase):

    # write a test for return_results function
    def test_return_results(self):
        testJSON = open('tests/resources/todaysScoreboard_00.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.return_results(data)
        self.assertEqual(response, {'0022200223': {'vteam_name': 'DET', 'hteam_name': 'LAC', 'vteam_score': 91, 'hteam_score': 96, 'score_diff': 5, 'game_summary_url': 'https://www.nba.com/game/DET-vs-LAC-0022200223?watch'}, '0022200221': {'vteam_name': 'BKN', 'hteam_name': 'POR', 'vteam_score': 109, 'hteam_score': 107, 'score_diff': 2, 'game_summary_url': 'https://www.nba.com/game/BKN-vs-POR-0022200221?watch'}})
    

    #def test_no_error_on_postponed_games(self):
    #    testJSON = open('tests/resources/PostponedGameAndNoCloseGame.json')
    #    data = json.load(testJSON)
    #    testJSON.close()
    #    response = app.check_close_game(data)
    #    self.assertEqual(response, {})

    #def test_no_error_on_postponed_games_and_no_close_game(self):
    #    testJSON = open('tests/resources/PostponedGameAndOT.json')
    #    data = json.load(testJSON)
    #    testJSON.close()
    #    response = app.check_close_game(data)
    #    self.assertEqual(response, {'game0': {'vteam_name': 'TOR', 'hteam_name': 'BKN', 'game_summary_url': 'https://www.nba.com/game/TOR-vs-BKN-0022100413?watch'}, 'game3': {'vteam_name': 'PHX', 'hteam_name': 'POR', 'game_summary_url': 'https://www.nba.com/game/PHX-vs-POR-0022100416?watch'}})

    #def test_correctly_identify_no_games_worth_watching(self):
    #    testJSON = open('tests/resources/NoGameWorthWatching.json')
    #    data = json.load(testJSON)
    #    testJSON.close()
    #    response = app.check_close_game(data)
    #    self.assertEqual(response, {})
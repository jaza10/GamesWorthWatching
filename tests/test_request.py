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
    #def test_check_close_game(self):

        # Sends API request, pot remove later
        #response = app.check_close_game(NBA_url)
        #self.assertEqual(response, ['ORL : LAC'])

    def test_no_error_on_postponed_games(self):
        testJSON = open('tests/resources/PostponedGameAndOT.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.check_close_game(data)
        self.assertEqual(response, ['TOR : BKN', 'PHX : POR'])

    def test_correctly_identify_no_games_worth_watching(self):
        testJSON = open('tests/resources/NoGameWorthWatching.json')
        data = json.load(testJSON)
        testJSON.close()
        response = app.check_close_game(data)
        self.assertEqual(response, [])



 


from flask import Flask, render_template
import requests
from datetime import date, timedelta, datetime

app = Flask(__name__)

TODAYS_SCOREBOARD = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
GAME_BOXSCORE = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
NBA_GAME_VIDEO_URL = "https://www.nba.com/game/{vteam_name}-vs-{hteam_name}-{game_id}?watch"


@app.route("/")
def main_function():
  # Making sure that right date is fetched each time page is requested, and results are not cached
  yesterday = date.today() - timedelta(1)
  response = requests.get(TODAYS_SCOREBOARD).json()
  # Checks if the json file doesn't contain results for yesterdays game yet
  if response["scoreboard"]["games"][0]["homeTeam"]["score"] == 0:
    return render_template("index.html", date = yesterday, results = return_results_from_yesterday(response))
  else:
    return render_template("index.html", date = yesterday, results = return_results_from_today(response))
    

def get_first_game_id(response):
    return response["scoreboard"]["games"][0]["gameId"]

# returns the string of the decremented game_id 
def decrement_game_id(game_id):
    game_id = int(game_id) - 1
    game_id = str(game_id).zfill(10)
    return game_id

# returns the boxscore of the requested game_id
def get_game_boxscore(game_id):
    game_url = GAME_BOXSCORE.format(game_id = game_id)
    response = requests.get(game_url).json()
    return response

# Given the boxscore of a game, it checks if the game happened yesterday
def check_if_game_is_from_yesterday(response):
    game_time = response["game"]["gameTimeLocal"]
    game_time = datetime.strptime(game_time,"%Y-%m-%dT%H:%M:%S%z")
    if game_time.day == datetime.today().day - 1:
        return True
    else:
        return False

# Checks if the game qualifies as a cloose and watchable game or not
# TODO: Extend by more criteria if a game is watchable or not, e.g. overtime, high score by a player, etc.
def check_if_it_was_a_close_game(response):
    vteam_score = response["game"]["awayTeam"]["score"]
    hteam_score = response["game"]["homeTeam"]["score"]
    if abs(vteam_score - hteam_score) <= 5 or response["game"]["period"] > 4: 
        return True
    else:
        return False

# write a function that collects the most important information about the game
def get_game_information(response):
    vteam_name = response["game"]["awayTeam"]["teamTricode"]
    hteam_name = response["game"]["homeTeam"]["teamTricode"]
    vteam_score = response["game"]["awayTeam"]["score"]
    hteam_score = response["game"]["homeTeam"]["score"]
    score_diff = abs(vteam_score - hteam_score)
    game_id = response["game"]["gameId"]
    game_summary_url = NBA_GAME_VIDEO_URL.format(vteam_name = vteam_name, hteam_name = hteam_name, game_id = game_id)
    game_information = {"vteam_name": vteam_name, "hteam_name": hteam_name, "vteam_score": vteam_score, "hteam_score": hteam_score, "score_diff": score_diff, "game_summary_url": game_summary_url}
    return game_information

def return_results_from_yesterday(response):
    results = {}
    first_game_id = get_first_game_id(response)
    yesterdays_last_game_id = decrement_game_id(first_game_id)
    game_boxscore = get_game_boxscore(yesterdays_last_game_id)
    while (check_if_game_is_from_yesterday(game_boxscore)):
        if check_if_it_was_a_close_game(game_boxscore):
            results[yesterdays_last_game_id] = get_game_information(game_boxscore)
        yesterdays_last_game_id = decrement_game_id(yesterdays_last_game_id)
        game_boxscore = get_game_boxscore(yesterdays_last_game_id)
    
    return results

def return_results_from_today(response):
    results = {}
    for game in response["scoreboard"]["games"]:
      vteam_score = game["awayTeam"]["score"]
      hteam_score = game["homeTeam"]["score"]
      score_diff = abs(vteam_score - hteam_score)
      if score_diff <= 5 or game["period"] > 4: # checks if game went to overtime
        vteam_name = game["awayTeam"]["teamTricode"]
        hteam_name = game["homeTeam"]["teamTricode"]
        game_id = game["gameId"]
        game_summary_url = NBA_GAME_VIDEO_URL.format(vteam_name = vteam_name, hteam_name = hteam_name, game_id = game_id)
        game_information = {"vteam_name": vteam_name, "hteam_name": hteam_name, "vteam_score": vteam_score, "hteam_score": hteam_score, "score_diff": score_diff, "game_summary_url": game_summary_url}
        results[game_id] = game_information
    # sort the results by score difference
    results = dict(sorted(results.items(), key=lambda item: item[1]["score_diff"]))
    return results
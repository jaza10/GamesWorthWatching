from flask import Flask, render_template
import requests
from datetime import date, timedelta

app = Flask(__name__)

TODAYS_SCOREBOARD = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
GAME_BOXSCORE = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
NBA_GAME_VIDEO_URL = "https://www.nba.com/game/{vteam_name}-vs-{hteam_name}-{game_id}?watch"


@app.route("/")
def get_yesterdays_date_and_json():
  # Making sure that right date is fetched each time page is requested, and results are not cached
  yesterday = date.today() - timedelta(1)
  yesterday_string = yesterday.strftime("%Y%m%d")
  NBA_url = NBA_URL.format(date = yesterday_string)
  response = requests.get(NBA_url).json()
  return render_template("index.html", date = yesterday, results = check_close_game(response))

# Function to check if game is close
def check_close_game(response):
    game_ids = get_game_ids(response)
    # check for each game if it is close
    results = {}
    for game_id in game_ids:
        game_url = NBA_GAME_ID_URL.format(game_id = game_id)
        game_response = requests.get(game_url).json()
        vteam_name = game_response["game"]["awayTeam"]["teamTricode"]
        hteam_name = game_response["game"]["homeTeam"]["teamTricode"]
        vteam_score = game_response["game"]["awayTeam"]["score"]
        hteam_score = game_response["game"]["homeTeam"]["score"]
        if abs(vteam_score - hteam_score) <= 5:
          game_summary_url = NBA_GAME_URL.format(vteam_name = vteam_name, hteam_name = hteam_name, game_id = game_id)
            # game_information = {"game_id": game_id, "vteam_name": vteam_name, "hteam_name": hteam_name, "vteam_score": vteam_score, "hteam_score": hteam_score, "game_summary_url": game_summary_url}
          game_information = {"vteam_name": vteam_name, "hteam_name": hteam_name, "game_summary_url": game_summary_url}
          results[game_id] = game_information
  
    return results
          
# write a function to get the hame IDs from the response
def get_game_ids(response):
    game_ids = []
    for game in response["games"]:
      game_ids.append(game["gameId"])
    return game_ids

def get_first_game_id(response):
    return response["scoreboard"]["games"][0]["gameId"]

def decrement_game_id(game_id):
    game_id = int(game_id) - 1
    game_id = str(game_id).zfill(10)
    return game_id
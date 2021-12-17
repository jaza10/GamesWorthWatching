from flask import Flask
import requests
from datetime import date, timedelta

app = Flask(__name__)

NBA_url_temp = "http://data.nba.net/10s/prod/v1/{date}/scoreboard.json"

@app.route("/")
def index():

  yesterday = date.today() - timedelta(1)
  yesterday_string = yesterday.strftime("%Y%m%d")
  NBA_url = NBA_url_temp.format(date = yesterday_string)
  return check_close_game(NBA_url, yesterday_string)

def check_close_game(url, date):
  response = requests.get(url)
  numGames = response.json().get("numGames")
  result = "Games worth watching on " + date + ": " 
  # TODO: include checks for NoneTypes and robust API requests
  # TODO: insert response for 0 games worth watching
  for i in range(numGames):
    try:
      game_vscore = int(response.json().get("games")[i]["vTeam"]["score"])
      game_hscore = int(response.json().get("games")[i]["hTeam"]["score"])
    except ValueError:
      pass
    score_difference = abs(game_vscore - game_hscore)
    if score_difference <= 6:
      vteam_name = response.json().get("games")[i]["vTeam"]["triCode"]
      hteam_name = response.json().get("games")[i]["hTeam"]["triCode"]
      result += vteam_name + " : " + hteam_name +", \n"
          
  return result


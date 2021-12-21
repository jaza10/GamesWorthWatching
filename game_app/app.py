from flask import Flask, render_template
import requests
from datetime import date, timedelta

app = Flask(__name__)

NBA_URL = "http://data.nba.net/10s/prod/v1/{date}/scoreboard.json"

@app.route("/")
def get_yesterdays_date_and_json():

  # Making sure that right date is fetched each time page is requested, and results are not cached
  yesterday = date.today() - timedelta(1)
  yesterday_string = yesterday.strftime("%Y%m%d")
  NBA_url_temp = NBA_URL.format(date = yesterday_string)
  response = requests.get(NBA_url_temp).json()
  return render_template("index.html", date = yesterday, results = check_close_game(response))

def check_close_game(response):
  numGames = response.get("numGames")
  result = []
  # TODO: Check period, current > 4 to detect OT games
  # TODO: Check isBuzzerBeater tag
  for i in range(numGames):
    try:
      game_vscore = int(response.get("games")[i]["vTeam"]["score"])
      game_hscore = int(response.get("games")[i]["hTeam"]["score"])
    except ValueError:
      pass
    score_difference = abs(game_vscore - game_hscore)
    if score_difference <= 6:
      vteam_name = response.get("games")[i]["vTeam"]["triCode"]
      hteam_name = response.get("games")[i]["hTeam"]["triCode"]
      result.append(vteam_name + " : " + hteam_name)
          
  return result
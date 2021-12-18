from flask import Flask, render_template
import requests
from datetime import date, timedelta

app = Flask(__name__)

NBA_url_temp = "http://data.nba.net/10s/prod/v1/{date}/scoreboard.json"

@app.route("/")
def index():

  # Making sure that right date is fetched each time page is requested, and results are not cached
  yesterday = date.today() - timedelta(1)
  yesterday_string = yesterday.strftime("%Y%m%d")
  NBA_url = NBA_url_temp.format(date = yesterday_string)
  return render_template("index.html", date = yesterday, results = check_close_game(NBA_url))

def check_close_game(url):
  response = requests.get(url)
  numGames = response.json().get("numGames")
  result = []
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
      result.append(vteam_name + " : " + hteam_name)
          
  return result
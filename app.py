from flask import Flask
import requests
from datetime import date, timedelta


app = Flask(__name__)


@app.route("/")

#today = date.today()
#today_string = today.strftime("%Y%m%d")
def index():

    yesterday = date.today() - timedelta(1)
    yesterday_string = yesterday.strftime("%Y%m%d")
    NBA_url = "http://data.nba.net/10s/prod/v1/{date}/scoreboard.json".format(date = yesterday_string)

    def check_close_game(url):
      response = requests.get(url)
      numGames = response.json().get("numGames")
      result = ""
      # TODO: include checks for NoneTypes and robust API requests
      for i in range(numGames):
        game_vscore = int(response.json().get("games")[i]["vTeam"]["score"])
        game_hscore = int(response.json().get("games")[i]["hTeam"]["score"])
        score_difference = abs(game_vscore - game_hscore)
        if score_difference <= 6:
          vteam_name = response.json().get("games")[i]["vTeam"]["triCode"]
          hteam_name = response.json().get("games")[i]["hTeam"]["triCode"]
          result += "Game worth watching: " + vteam_name + " : " + hteam_name +" \n"
        #TODO: Return list of games worth watching
    
      return result

    return check_close_game(NBA_url)

#    return "Congratulations, it's a web app!"





#check_close_game(NBA_url)

#if __name__ == "__main__":
#    app.run(host="127.0.0.1", port=8080, debug=True)

import requests
import json
from datetime import date, datetime, time
import dateutil.parser

token = "YOURTOKEN"

url = "https://api.pandascore.co/lol/matches/upcoming?filter[league_id]=293"#293 is LCK

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}

def get_lck_schedule():
     out_list = []
     response = requests.request("GET", url, headers=headers)

     data = json.loads(response.text)

     for match in data:
          tmp_date = match["scheduled_at"]
          date = dateutil.parser.isoparse(tmp_date[:-1] + '+00:00')
          team1 = match["opponents"][0]["opponent"]["name"]
          team2 = match["opponents"][1]["opponent"]["name"]
          if (abs((datetime.today() - date.replace(tzinfo=None)).total_seconds()) < 86400):
               print("LCK")
               out_list.append(["LCK",team1,team2])

     return out_list

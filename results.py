import csv
    

import requests

import json
from datetime import date, datetime, time
from difflib import SequenceMatcher


def get_team_names_old(team1, team2, teams):
    team1_ratio = 0
    team2_ratio = 0
    wanted_team1 = ""
    wanted_team2 = ""
    for team in teams:
        tmp1 = SequenceMatcher(None, team1.lower(), team.lower()).ratio()
        tmp2 = SequenceMatcher(None, team2.lower(), team.lower()).ratio()
        if "Academy" not in team:
          if tmp1 > team1_ratio:
              wanted_team1 = team
              team1_ratio = tmp1
          if tmp2 > team2_ratio:
              wanted_team2 = team
              team2_ratio = tmp2
    return [wanted_team1, wanted_team2]

with open("/srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/lol_esports-predictions/results.csv", "r", newline='') as file:
    reader = csv.reader(file)
    predictions = list(reader)


url ='https://api.pandascore.co/lol/matches/past?sort=&page=1&per_page=100'

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer XXXXXXXXXXXXXXX"
}

response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)
all_panda_teams = []

panda_matches = []

for match in data:
  team1 = match["opponents"][0]["opponent"]["name"]
  team2 = match["opponents"][1]["opponent"]["name"]
  all_panda_teams.append(team1)
  all_panda_teams.append(team2)
  date = match["original_scheduled_at"]
  if(match["winner"]):
    winner = match["winner"]["name"]
    panda_matches.append([team1,team2,winner,date])

all_panda_teams = set(all_panda_teams)

end_results = []
for line in predictions:
  if line[9] == "":
    latest = datetime.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    latest_match = ""
    t1 = line[0]
    t2 = line[1]
    team1, team2 = get_team_names_old(t1,t2,all_panda_teams)
    for p in panda_matches:
      if p[0] == team1 and p[1] == team2:
        output_date = datetime.strptime(p[3], "%Y-%m-%dT%H:%M:%SZ")
        if output_date > latest:
          latest = output_date
          latest_match = p

      if p[1] == team1 and p[0] == team2:
        output_date = datetime.strptime(p[3], "%Y-%m-%dT%H:%M:%SZ")
        if output_date > latest:
          latest = output_date
          latest_match = p
  



    
  
  
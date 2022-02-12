import csv
import os
import shutil

from datetime import date
from difflib import SequenceMatcher
from get_team_stats import download_week
from predict import predict
from predict_request import predict_akkio
from scheduler import get_matches_today
from team_data_parser import parse_teams, data_for_prediction
'''
Obtains tflearn and akkio predictions and writes them to a csv file
p1: list of tflearn predictions [[teamname1, t1_win, teamname2, t2_win][...]]
p2: list of akkio predictions [[teamname1, t1_win, teamname2, t2_win][...]]
'''


def write_results(p1, p2):
    data_to_write = []

    for idx, prediction in enumerate(p1):
        winner_tf = ""
        winner_akkio = ""

        #If t1 has a higher winchance
        if (prediction[1] > prediction[3]):
            winner_tf = prediction[0]
        else:
            winner_tf = prediction[2]

        if (p2[idx][1] > p2[idx][3]):
            winner_akkio = p2[idx][0]
        else:
            winner_akkio = p2[idx][2]

        #Holds a row of the output file
        data_to_write.append([
            prediction[0], prediction[2],
            date.today().strftime("%d/%m/%Y"),
            round(prediction[1], 3),
            round(prediction[3], 3),
            round(p2[idx][1], 3),
            round(p2[idx][3], 3), winner_tf, winner_akkio, "", ""
        ])

    #Actually appends the new predictions
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_to_write)


'''
Depracted for now, otherwise is very useful to match similar strings such as team names
'''


def get_team_names_old(team1, team2):
    with open("team_out.csv", newline='') as f:
        reader = csv.reader(f)
        teams = list(reader)
    team1_ratio = 0
    team2_ratio = 0
    wanted_team1 = ""
    wanted_team2 = ""
    for team in teams:
        tmp1 = SequenceMatcher(None, team1.lower(), team[0].lower()).ratio()
        tmp2 = SequenceMatcher(None, team2.lower(), team[0].lower()).ratio()
        if tmp1 > team1_ratio:
            wanted_team1 = team[0]
            team1_ratio = tmp1
        if tmp2 > team2_ratio:
            wanted_team2 = team[0]
            team2_ratio = tmp2
    return [wanted_team1, wanted_team2]


'''
Matches teamnames from calendar to the ones from OE.
'''


def get_team_names(team1, team2):
    team_dic = {
        "EG": "Evil Geniuses",
        "DIG": "Dignitas",
        "IMT": "Immortals",
        "100": "100 Thieves",
        "TL": "Team Liquid",
        "C9": "Cloud9",
        "GG": "Golden Guardians",
        "CLG": "Counter Logic Gaming",
        "TSM": "TSM",
        "FLY": "FlyQuest",
        "RGE": "Rogue",
        "AST": "Astralis",
        "VIT": "Team Vitality",
        "XL": "Excel Esports",
        "BDS": "Team BDS",
        "MSF": "Misfits Gaming",
        "SK": "SK Gaming",
        "FNC": "Fnatic",
        "MAD": "MAD Lions",
        "G2": "G2 Esports"
    }
    return [team_dic[team1], team_dic[team2]]


#Lists all matches of the day
today = get_matches_today()
teams_to_find_data = []
if today:
    #Remove old data csv
    if os.path.exists("lcs_team_in.csv"):
        os.remove("lcs_team_in.csv")
    if os.path.exists("lec_team_in.csv"):
        os.remove("lec_team_in.csv")
    if os.path.exists("lck_team_in.csv"):
        os.remove("lck_team_in.csv")
    #Gets the latest team averages
    lcs_file = download_week("LCS")
    lec_file = download_week("LEC")
    lck_file = download_week("LCK")
    #Move the data to the current directory
    shutil.move(lcs_file, "./lcs_team_in.csv")
    shutil.move(lec_file, "./lec_team_in.csv")
    shutil.move(lck_file, "./lck_team_in.csv")
    #Transforms team data into data to feed the predictor
    parse_teams()
    #For each map
    for team in today:
        #Special treatment for LCK as their schedule is obtained differently
        if team[0] == "LCK":
            team1_name, team2_name = get_team_names_old(team[1], team[2])
        else:
            #Obtain right names to match OE's csv
            team1_name, team2_name = get_team_names(team[0], team[1])
        teams_to_find_data.append([team1_name, team2_name])
    #Holds the correctly formated team stats to feed the predictor
    data_for_prediction = data_for_prediction(teams_to_find_data)
    #Predicts using tflearn
    p1 = predict(data_for_prediction)
    #Predicts using Akkio
    p2 = predict_akkio(data_for_prediction)
    #Stores/writes the results
    write_results(p1, p2)

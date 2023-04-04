import csv
import os
import glob
import shutil
import sys

from datetime import date
from difflib import SequenceMatcher
from get_team_stats import download_oe_data, download_custom_oe_data
from predict import predict
from predict_request import predict_akkio
from scheduler import get_matches_today
from team_data_parser import parse_teams, data_for_prediction, merge_team_entries
from parse_players import player_data_for_prediction, parse_player_data
from predict_players import predict_players
'''
Obtains tflearn and akkio predictions and writes them to a csv file
p1: list of tflearn predictions [[teamname1, t1_win, teamname2, t2_win][...]]
p2: list of akkio predictions [[teamname1, t1_win, teamname2, t2_win][...]]
'''


def write_results(p1, p2, p3):
    data_to_write = []

    for idx, prediction in enumerate(p1):
        winner_tf = ""
        winner_akkio = ""
        winner_player = ""

        #If t1 has a higher winchance
        if (prediction[1] > prediction[3]):
            winner_tf = prediction[0]
        else:
            winner_tf = prediction[2]

        if (p2[idx][1] > p2[idx][3]):
            winner_akkio = p2[idx][0]
        else:
            winner_akkio = p2[idx][2]

        if (p3[idx][1] > p3[idx][3]):
            print("Winner is " + p3[idx][0])
            print("With winrate" + str(p3[idx][1]))
            winner_player = p3[idx][0]
        else:
            print("Winner is " + p3[idx][2])
            print("With winrate" + str(p3[idx][3]))
            winner_player = p3[idx][2]

        print(p3[idx])
        print(p3[idx])
        if p3[idx][0] == prediction[0]:
            p3_left_winrate = p3[idx][1]
        else:
            p3_left_winrate = p3[idx][3]
        #Holds a row of the output file
        data_to_write.append([
            prediction[0], prediction[2],
            date.today().strftime("%d/%m/%Y"),
            round(prediction[1], 5),
            round(p2[idx][1], 5),
            round(p3_left_winrate, 5), #Reversed order of teams for some reason (probs due to appends)
            winner_tf, 
            winner_akkio,
            winner_player, 
            "", 
            "",
            ""
        ])

    #Actually appends the new predictions
    print("writing to nongit results:")
    print(data_to_write)
    with open('./results.csv', 'w', newline='') as csvfile:
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
        "G2": "G2 Esports",
        "BRO" : "BRION",
        "KT" : "KT Rolster",
        "LSB" : "Liiv SANDBOX",
        "NS" : "Nongshim RedForce",
        "GEN" : "Gen.G",
        "HLE" : "Hanwha Life Esports",
        "KDF" : "Kwangdong Freecs",
        "DK" : "Dplus KIA",
        "DRX" : "DRX",
        "T1" : "T1",
        "RED" : "RED Canids",
        "PSG" : "PSG Talon",
        "IW" : "İstanbul Wildcats",
        "RNG" : "Royal Never Give Up",
        "ORD" : "ORDER",
        "AZE" : "Team Aze",
        "DFM" : "DetonatioN FocusMe",
        "SGB" : "Saigon Buffalo",
        "LLL" : "LOUD",
        "ISG" : "Isurus",
        "BYG" : "Beyond Gaming",
        "CHF" : "Chiefs Esports Club",
        "EDG" : "EDward Gaming",
        "JDG" : "JD Gaming",
        "GAM" : "GAM Esports",
        "CFO" : "CTBC Flying Oyster",
        "TES" : "Top Esports",
        "KOI" : "KOI",
        "TH"  : "Team Heretics"
    }
    return [team_dic[team1], team_dic[team2]]



print("start logic")
custom_predict = False
international = False
if len(sys.argv) > 1:
    custom_predict = True
    cT1 = sys.argv[1]
    cT2 = sys.argv[2]
    cStart = sys.argv[3] + " " + sys.argv[4]
    cEnd = sys.argv[5] + " " + sys.argv[6]
    cRegion = sys.argv[7]
    cSeason = sys.argv[8]



if (custom_predict):
    if ("international" in cRegion):
        international = True
print("start logic 2 ")


#Lists all matches of the day
print("--------")
today = get_matches_today()
teams_to_find_data = []
print("Received today: ")
print(today)
print("start logic3")

if today or custom_predict:
    print("in today")
    print(today)
    if custom_predict:
        playoffs_regions = [cRegion]
    else:
        playoffs_regions = []
    #Remove old playoff data
    for match in today:
        if len(match) > 2:
            if match[3] not in playoffs_regions:
                playoffs_regions.append(match[3])
            if os.path.exists(match[3] + "_team_playoffs_in.csv"):
                os.remove(match[3] + "_team_playoffs_in.csv")
    #Remove old data csv
    if os.path.exists("lcs_team_in.csv"):
        os.remove("lcs_team_in.csv")
    if os.path.exists("lec_team_in.csv"):
        os.remove("lec_team_in.csv")
    if os.path.exists("lck_team_in.csv"):
        os.remove("lck_team_in.csv")
    #Gets the latest team averages
    print("before team data")
    files = []
    try:
        if custom_predict:
            if international:
                for reg in ["LCS","LEC","LCK","VCS","LLA","LJL","LCO","TCL","LPL","CBLOL","PCS"]:
                    files.append(download_custom_oe_data("teams", reg, cSeason, cStart, cEnd))
            else:
                files.append(download_custom_oe_data("teams", cRegion, cSeason, cStart, cEnd))
        else:
            files.append(download_oe_data("teams", "LCS"))
            files.append(download_oe_data("teams", "LEC"))
            files.append(download_oe_data("teams", "LCK"))
            #files.append(download_oe_data("teams", "World Championship", "Season"))

        for region in playoffs_regions:
            if international:
                for reg in ["LCS","LEC","LCK","VCS","LLA","LJL","LCO","TCL","LPL","CBLOL","PCS"]:
                    files.append(download_custom_oe_data("teams", reg, cSeason, cStart, cEnd))


    except Exception as e:
        print(e)
        exit()
    print("got team data")
    print(files)
    #Move the data to the current directory
    for file in files:
        if "Playoffs" in file and not custom_predict:
            desired_name = "./" + os.path.basename(file)[0:3].lower() + "_team_playoffs_in.csv"
        elif file == "nothing":
            continue
        else:
            desired_name = "./" + os.path.basename(file)[0:3].lower() + "_team_in.csv"
            print("Moving" + desired_name)
        shutil.move(file, desired_name)

    #Transforms team data into data to feed the predictor
    print("Parsing teams")
    parse_teams()
    for match in today:
        if len(match) > 2:
            merge_team_entries()
            break
    print("Parsing player data")
    parse_player_data()
    #For each map
    for team in today:
        #Special treatment for LCK as their schedule is obtained differently
        if team[0] == "LCK":
            team1_name, team2_name = get_team_names_old(team[1], team[2])
        else:
            #Obtain right names to match OE's csv
            team1_name, team2_name = get_team_names(team[0], team[1])
        print("inside loop")
        print([team1_name, team2_name])
        teams_to_find_data.append([team1_name, team2_name])
    if custom_predict:
        teams_to_find_data.append([cT1, cT2])
    print("Teams for data: ")
    print(teams_to_find_data)
    #Holds the correctly formated team stats to feed the predictor
    if custom_predict:
        new_teams_to_find_data = []
        for team in teams_to_find_data:
            new_teams_to_find_data.append(get_team_names(team[0], team[1]))
        data_for_prediction = data_for_prediction(new_teams_to_find_data)

    else:
        data_for_prediction = data_for_prediction(teams_to_find_data)
    print("-----------teams_to_find_data")
    print(teams_to_find_data)
    print(data_for_prediction)
    print("-----------")
    if custom_predict:
        new_teams_to_find_data = []
        for team in teams_to_find_data:
            new_teams_to_find_data.append(get_team_names(team[0], team[1]))
        player_data_for_prediction = player_data_for_prediction(new_teams_to_find_data, today, True, cSeason, cRegion, cStart, cEnd)
    else:
        player_data_for_prediction = player_data_for_prediction(teams_to_find_data, today, False, None, None, None, None)
    #print("Predicitng thus: ")
    #print(data_for_prediction)
    #Predicts using tflearn
    p1 = predict(data_for_prediction)
    #Predicts using Akkio
    p2 = predict_akkio(data_for_prediction)
    #Predicts using tflearn on player data
    p3 =  predict_players(player_data_for_prediction)
    print(p1)
    print(p2)
    print(p3)
    print("Done and writin results")
    #Stores/writes the results
    write_results(p1, p1, p3)
else:
    exit(1)

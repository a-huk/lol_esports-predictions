import csv
import glob
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
'''
Formats the team data the right way, that is needed for the predictions.
It is somewhat a mess
'''


def parse_teams():
    if os.path.exists("team_out.csv"):
        os.remove("team_out.csv")

    team_in_files = glob.glob("*team_in.csv")

    for file in team_in_files:
        print("Doing "+ file)
        with open(file, newline='') as f:
            reader = csv.reader(f)
            starting_data = list(reader)

        labels = starting_data.pop(0)
        out_data = [[
            "Team", "GP", "K", "D", "GL", "CKPM", "GPR", "GD15", "FB", "FT",
            "F3T", "PPG", "HLD", "FD", "DRG", "ELD", "BN", "FBN", "LNE", "JNG",
            "WPM", "CWPM", "WCPM"
        ]]

        for team in tqdm(starting_data, desc ="Parsing teams"):
            teamname = team[0]
            games_played = int(team[1])
            kills_per_game = float(team[5]) / games_played
            deaths_per_game = float(team[6]) / games_played
            game_length = team[4]
            ckpm = team[8]
            gpr = team[9]
            gspd = float(team[10].replace("%", "")) / 100
            gd15 = team[13]
            firstblood = float(team[14].replace("%", "")) / 100
            firsttower = 0.3
            if team[15] != "":
                firsttower = float(team[15].replace("%", "")) / 100

            first3towers = 0.3
            if team[16] != "":
                first3towers = float(team[16].replace("%", "")) / 100
            turret_plates_per_game = team[17]
            harold_control_rate = 0.3
            if team[18] != "":
                harold_control_rate = float(team[18].replace("%", "")) / 100
            firstdragon = 0.3
            if team[19] != "":
                firstdragon = float(team[19].replace("%", "")) / 100
            dragon_control_rate = 0.3
            if team[20] != "":
                dragon_control_rate = float(team[20].replace("%", "")) / 100
            elder_control_rate = 0.3
            if team[21] != "":
                elder_control_rate = float(team[21].replace("%", "")) / 100
            baron_control_rate = float(team[23].replace("%", "")) / 100
            firstbaron = 0.3
            if team[22] != "":
                firstbaron = float(team[22].replace("%", "")) / 100
            cs_share = float(team[24].replace("%", "")) / 100
            jng_share = float(team[25].replace("%", "")) / 100
            wards_per_minute = team[26]
            control_wards_purchased_per_minute = team[27]
            wards_cleared_per_minute = team[28]
            out_data.append([
                teamname, kills_per_game, deaths_per_game, game_length, ckpm,
                gpr, gspd, gd15, firstblood, firsttower, first3towers,
                turret_plates_per_game, harold_control_rate, firstdragon,
                dragon_control_rate, elder_control_rate, baron_control_rate,
                firstbaron, cs_share, jng_share, wards_per_minute,
                control_wards_purchased_per_minute, wards_cleared_per_minute
            ])

        #Write or append to file
        if os.path.exists("team_out.csv"):
            with open('team_out.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(out_data)
        else:
            with open('team_out.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(out_data)
    #Clean up
    for file in team_in_files:
        os.remove(file)


def data_for_prediction(match_list):
    data = []
    with open('team_out.csv', newline='') as f:
        reader = csv.reader(f)
        all_data = list(reader)
        for match in match_list:
            tmp_data = []
            tmp_data2 = []
            team1 = match[0]
            team2 = match[1]
            for team in all_data:
                if team[0] == team1:
                    tmp_data.append(team[1:])
                    tmp_data2.append(team1)
                elif team[0] == team2:
                    tmp_data.append(team[1:])
                    tmp_data2.append(team2)
            left_first = [item for sublist in tmp_data for item in sublist]
            tmp_data.reverse()
            right_first = [item for sublist in tmp_data for item in sublist]
            data.append([left_first] + [right_first] + tmp_data2)
    return data

def merge_team_entries():
    data = []
    with open('team_out.csv', newline='') as f:
        reader = csv.reader(f)
        all_data = list(reader)

    for idx, entry in enumerate(all_data):
        if idx != 0:
            for idx2, entry2 in enumerate(all_data):
                if entry[1] == "GP":
                    continue
                if entry[0] == entry2[0] and idx != idx2:
                    new_line = [entry]
                    data.append(new_line.extend([(g + h) / 2 for g, h in zip(entry[1:], entry2[1:])]))
                    break
                else:
                    data.append(entry)
                    break

    with open('team_out.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)

"""def parse_teams_2():
    if os.path.exists("team_out.csv"):
        os.remove("team_out.csv")

    team_in_files = glob.glob("*team_in.csv")

    for file in team_in_files:
        df = pd.read_csv(file)

        #labels = df.key()
        out_df = pd.DataFrame(columns=[
            "Team", "GP", "K", "D", "GL", "CKPM", "GPR", "GD15", "FB", "FT",
            "F3T", "PPG", "HLD", "FD", "DRG", "ELD", "BN", "FBN", "LNE", "JNG",
            "WPM", "CWPM", "WCPM"
        ])

        for index in df.index:
            teamname = df["Team"][index]
            games_played = df["GP"][index]
            kills_per_game = df["K"][index] / games_played
            deaths_per_game = df["D"][index] / games_played
            game_length = df["AGT"][index]
            ckpm = df["CKPM"][index]
            gpr = df["GPR"][index]
            gspd = df["GSPD"][index].replace("%", "").astype(float) / 100
            gd15 = df["GD15"][index]
            firstblood = df["FB%"][index].replace("%", "").astype(float) / 100
            firsttower = df["FT%"][index].replace("%", "").astype(float) / 100
            first3towers = df["F3T%"][index].replace("%", "").astype(float) / 100
            turret_plates_per_game = df["PPG"][index]
            harold_control_rate = df["HLD%"][index].replace("%", "").astype(float) / 100
            firstdragon = df["FD%"][index].replace("%", "") / 100
            dragon_control_rate = df["DRG%"][index].replace("%", "").astype(float) / 100
            elder_control_rate = 0.3
            if not pd.isnull(df["ELD%"][index]):
                elder_control_rate = df["ELD%"][index].replace("%", "").astype(float) / 100
            baron_control_rate = df["BN%"][index].replace("%", "").astype(float) / 100
            firstbaron = df["FBN%"][index].replace("%", "").astype(float) / 100
            cs_share = df["LNE%"][index].replace("%", "").astype(float) / 100
            jng_share = df["JNG%"][index].replace("%", "").astype(float) / 100
            wards_per_minute = df["WPM"][index]
            control_wards_purchased_per_minute = df["CWPM"][index]
            wards_cleared_per_minute = df["WCPM"][index]
            out_df = out_df.append(pd.DataFrame([[
                teamname, kills_per_game, deaths_per_game, game_length, ckpm,
                gpr, gspd, gd15, firstblood, firsttower, first3towers,
                turret_plates_per_game, harold_control_rate, firstdragon,
                dragon_control_rate, elder_control_rate, baron_control_rate,
                firstbaron, cs_share, jng_share, wards_per_minute,
                control_wards_purchased_per_minute, wards_cleared_per_minute
            ]], columns=out_df.columns), ignore_index=True)


        #Write or append to file
        if os.path.exists("team_out.csv"):
            out_df.to_csv('team_out.csv', index=False, mode="a")
        else:
            out_df.to_csv('team_out.csv', index=False)
    #Clean up
    #for file in team_in_files:
    #    os.remove(file)"""


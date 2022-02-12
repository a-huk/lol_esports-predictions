import csv
import glob
import os
'''
Formats the team data the right way, that is needed for the predictions.
It is somewhat a mess
'''


def parse_teams():
    if os.path.exists("team_out.csv"):
        os.remove("team_out.csv")

    team_in_files = glob.glob("*team_in.csv")

    for file in team_in_files:
        with open(file, newline='') as f:
            reader = csv.reader(f)
            starting_data = list(reader)

        labels = starting_data.pop(0)
        out_data = [[
            "Team", "GP", "K", "D", "GL", "CKPM", "GPR", "GD15", "FB", "FT",
            "F3T", "PPG", "HLD", "FD", "DRG", "ELD", "BN", "FBN", "LNE", "JNG",
            "WPM", "CWPM", "WCPM"
        ]]

        for team in starting_data:
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
            firsttower = float(team[15].replace("%", "")) / 100
            first3towers = float(team[16].replace("%", "")) / 100
            turret_plates_per_game = team[17]
            harold_control_rate = float(team[18].replace("%", "")) / 100
            firstdragon = float(team[19].replace("%", "")) / 100
            dragon_control_rate = float(team[20].replace("%", "")) / 100
            elder_control_rate = 0.3
            if team[21] != "":
                elder_control_rate = float(team[21].replace("%", "")) / 100
            baron_control_rate = float(team[23].replace("%", "")) / 100
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
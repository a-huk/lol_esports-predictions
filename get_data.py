import csv
import oracles_elixir as oe
import os
'''
Function that transfors a team line data from the OE csv dataset to a list of all target data values
line: csv row of first team of a given match
line2: csv row of second team of a given match
return: list of values for a given team/match
'''


def line2final(line, line2):
    kills_per_game = line[26]
    deaths_per_game = line[27]
    game_length = float(line[24]) / 60  #in minutes
    ckpm = line[40]
    gpr = float(line[82]) / (float(line[82]) + float(line2[82]))
    gspd = line[87]
    gd15 = line[115]
    firstblood = line[35]
    firsttower = line[61]
    first3towers = line[65]
    turret_plates_per_game = line[66]
    harold_control_rate = 0
    if line[56] != "0.0":
        harold_control_rate = float(
            line[56]) / (float(line[56]) + float(line2[56]))
    firstdragon = line[41]
    dragon_control_rate = 0
    if line[42] != "0.0":
        dragon_control_rate = float(
            line[42]) / (float(line[42]) + float(line2[42]))
    if line[53] == "0.0" and line2[53] == "0.0":
        elder_control_rate = 0.5
    else:
        elder_control_rate = float(
            line[53]) / (float(line[53]) + float(line2[53]))
    if line[59] == "0.0" and line2[59] == "0.0":
        baron_control_rate = 0.5
    else:
        baron_control_rate = float(
            line[59]) / (float(line[59]) + float(line2[59]))
    firstbaron = line[58]
    cs_share = float(line[89]) / (float(line[89]) + float(line2[89]))
    jng_share = float(line[90]) / (float(line[90]) + float(line2[90]))
    wards_per_minute = line[76]
    control_wards_purchased_per_minute = float(line[79]) / game_length
    wards_cleared_per_minute = line[78]
    return [
        kills_per_game, deaths_per_game, game_length, ckpm, gpr, gspd, gd15,
        firstblood, firsttower, first3towers, turret_plates_per_game,
        harold_control_rate, firstdragon, dragon_control_rate,
        elder_control_rate, baron_control_rate, firstbaron, cs_share,
        jng_share, wards_per_minute, control_wards_purchased_per_minute,
        wards_cleared_per_minute
    ]


#Download and save the latest data
oe_data = oe.download_data()
oe_data.to_csv("all_data.csv")

#Only append team data from initial csv as opposed to player data
with open('all_data.csv', newline='') as f:
    reader = csv.reader(f)
    starting_data = list(reader)
only_team_data = []
for line in starting_data:
    if line[13] == "team":
        #Additional integrity checking
        if line[89] != "":  #Remove teams with empty cs_share
            only_team_data.append(line)

#Add two teams data and write out the resulting amtches and results in all_out.csv
ready_all_data = []
first_part = True
for index, line in enumerate(only_team_data):
    if first_part:  #left right to result
        ready_all_data.append(
            [line[25]] + line2final(line, only_team_data[index + 1]) +
            line2final(only_team_data[index + 1], line))  #add win of left team
        first_part = False
    else:
        first_part = True

os.remove("all_data.csv")

with open('all_out.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "left_win", "kills_per_game", " deaths_per_game", " game_length",
        " ckpm", " gpr", " gspd", " gd15", " firstblood", " firsttower",
        " first3towers", " turret_plates_per_game", " harold_control_rate",
        " firstdragon", " dragon_control_rate", " elder_control_rate",
        " baron_control_rate", " firstbaron", " cs_share", " jng_share",
        " wards_per_minute", " control_wards_purchased_per_minute",
        " wards_cleared_per_minute", "kills_per_game", " deaths_per_game",
        " game_length", " ckpm", " gpr", " gspd", " gd15", " firstblood",
        " firsttower", " first3towers", " turret_plates_per_game",
        " harold_control_rate", " firstdragon", " dragon_control_rate",
        " elder_control_rate", " baron_control_rate", " firstbaron",
        " cs_share", " jng_share", " wards_per_minute",
        " control_wards_purchased_per_minute", " wards_cleared_per_minute"
    ])
    writer.writerows(ready_all_data)
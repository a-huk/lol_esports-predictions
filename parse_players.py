import csv 
import time
import glob
import os
from get_team_stats import download_oe_data, download_custom_oe_data
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing.pool as mpp
from itertools import repeat
import gc
from datetime import datetime
from contextlib import closing

def parse_player_data():
    with open('./all_data.csv', newline='') as f:
        reader = csv.reader(f)
        starting_data = list(reader)

    starting_data.pop(0) #Remove headers
    last_five = [] #Holds 5 players in a team
    positions = []
    player_count = 0 #Count to 5
    current_game_id = "none" 
    faulty_matches = []
    games = {}

    print("Preparing teams")
    for line in starting_data:
        position = line[13]
        if position != "team" and line[72] != "" and line[71] != "" and line[93] != "": #Only players and that have complete data
            if player_count == 5 and len(positions) == 5 and "top" in positions and "jng" in positions and "mid" in positions and "bot" in positions and "sup" in positions: #Once we have 'accumulated' five players with all the right positions
                if current_game_id in games:
                    if position == "team":
                        print("fail")
                        exit()
                    games[current_game_id] = [games[current_game_id], last_five]
                else:
                    if position == "team":
                        print("fail1")
                        exit()
                    games[current_game_id] = last_five
                last_five = [] #Reset values
                positions = []
                player_count = 0
                current_game_id = "none"
            #Accumulating a player
            if current_game_id == "none": 
                current_game_id = line[1]
            playername = line[14]
            position = line[13]
            positions.append(position)
            last_five.append(playername)
            player_count += 1

    #Weed out bad teams or entries without 5 players
    print("Weeding out bad entries")
    for key in list(games):
        for team in games[key]:
            if len(team) != 5:
                if key in games:
                    del games[key]
                    continue

    tmp = games
    lines_in = []
    #Convert list to dict
    starting_data_dict = {}
    for line in tqdm(starting_data, desc="Converting starting data to dictionary"):
        starting_data_dict[line[1]+line[14]] = line

    for key in tqdm(games, desc="Final part of player parsing"):
    #tab once until with open
        found_result = False
        game_line = []
        skip_row = False
        for team in games[key]:
            game_id = key
            for player in team:
                found_player = False
                line = starting_data_dict[game_id+player]
                position = line[13]
                if position == "team":
                    skip_row = True
                    break
                found_player = True
                if not found_result:
                    result = line[25]
                    found_result = True
                    game_line.append(result)
                #Data we want:
                kills = line[26]
                deaths = line[27]
                assists = line[28]
                if line[29] == "0":
                    kp = "0"
                else:
                    kp = str( (int(kills) + int(assists))/int(line[29]) )
                if line[30] == "0":
                    dth = "0"
                else:
                    dth = str( (int(deaths)/int(line[30]) ))
                if line[35] == "":
                    fb = str(0)
                else:
                    fb = line[35]
                if line[100] == "":
                    gd10 = str(0)
                else:
                    gd10 = line[100]
                if line[101] == "":
                    xpd10 = str(0)
                else:
                    xpd10 = line[101]
                        
                if line[102] == "":
                    csd10 = str(0)
                else:
                    csd10 = line[102]
                cspm = line[93]
                dpm = line[71]
                egpm = line[84]
                goldshare = line[85]
                wpm = line[76]
                wcpm = line[78]
                game_line.append([kills, deaths, assists, kp, dth, fb, gd10, xpd10, csd10, cspm, dpm,  egpm, goldshare, wpm, wcpm])
                if not found_player:
                    print("Failed to find player")
                    exit()
            if skip_row:
                break
        if skip_row:
            continue
        lines_in.append([item for sublist in game_line for item in sublist])
    print(len(lines_in))
    with open('player_out.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines_in)

    #pool = Pool(os.cpu_count()-1)
    """    for _ in tqdm(pool.imap_unordered(multiprocess_faster, tmp,tl), total=len(tmp), desc="Final part of player parsing"):
        pass"""
    #t1 = datetime.now()
    #with closing( Pool(os.cpu_count()-1,maxtasksperchild=1) ) as p:
    #    p.imap(multiprocess_faster, zip(games, repeat(games), repeat(starting_data)))
    #print(str(datetime.now()-t1))
    
    #for _ in tqdm(pool.starmap(multiprocess_faster, zip(games, repeat(games), repeat(starting_data))), total=len(tmp), desc="Final part of player parsing"):
    #    pass
    #pool.close()
    #pool.join()
    


def player_data_for_prediction(teams, matches, custom_predict, season, region, start, end):
    
    files = []
    regions_with_playoffs = []

    for match in matches:
        if len(match) > 2:
            if match[3] not in regions_with_playoffs:
                regions_with_playoffs.append(match[3])

    dfiles = glob.glob('/root/Downloads/*')
    if dfiles:
        for f in dfiles:
            os.remove(f)

    if custom_predict:
        if "international" in region:
                for reg in ["LCS","LEC","LCK","VCS","LLA","LJL","LCO","TCL","LPL","CBLOL","PCS"]:
                    files.append(download_custom_oe_data("players", reg, season, start, end))

    else:   
        lck_players_file = download_oe_data("players", "LCK")
        lcs_players_file = download_oe_data("players", "LCS")
        lec_players_file = download_oe_data("players", "LEC")
        #worlds_players_file = download_oe_data("players", "World Championship", "Season")
    
        for region in regions_with_playoffs:
            files.append(download_oe_data("players", region, "Playoffs"))
    

    all_player_data = []

    print("------------------------")
    print(custom_predict)
    print(files)
    print("nothing" in files)
    print("------------------------")
    
    if not custom_predict:
        with open(lcs_players_file, newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
                for x in data:
                    all_player_data.append(x)
        f.close()

        with open(lec_players_file, newline='') as f1:
                reader = csv.reader(f1)
                data1 = list(reader)
                for y in data1:
                    all_player_data.append(y)
        f1.close()
                
        with open(lck_players_file, newline='') as f2:
                 reader = csv.reader(f2)
                 data2 = list(reader)
                 for z in data2:
                     all_player_data.append(z)
        f2.close()

        #with open(worlds_players_file, newline='') as f3:
        #        reader = csv.reader(f3)
        #        data3 = list(reader)
        #        for o in data3:
        #            all_player_data.append(o)
        #f3.close()

    else:
        for file in files:
            if file != "nothing":
                with open(file, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    for x in data:
                        all_player_data.append(x)
                f.close()



    playoff_players = []
    if not custom_predict:
        for file in files:
            if file != "nothing":
                with open(file, newline='') as f:
                     reader = csv.reader(f)
                     data = list(reader)
                f.close()
                for player in data:
                    playoff_players.append(player)

    
    predict_in = []

    for team in teams:
        pred_row = []
        team1 = team[0]
        team2 = team[1]
        for t in team:
            for role in ["Top", "Jungle", "Middle", "ADC", "Support"]:
                for line in all_player_data:
                    if line[1] == t and role == line[2]:
                        
                        if line[0] in playoff_players:
                            for player in playoff_players:
                                if line[0] == player[0]:
                                    kills = str(( float(line[6] ) + float(player[6])) / 2 )
                                    deaths = str(( float(line[7]) + float(player[7])) / 2 )
                                    assists = str(( float(line[8]) + float(player[8])) / 2 )
                                    kp = str((float(line[10].split("%")[0])/100 + float(player[10].split("%")[0])/100)/2)
                                    dth = str((float(line[12].split("%")[0])/100 + float(player[12].split("%")[0])/100)/2)
                                    fb = str((float(line[13].split("%")[0])/100 + float(player[13].split("%")[0])/100)/2)
                                    gd10 = str(( float(line[14]) + float(player[14])) / 2 )
                                    xpd10 = str(( float(line[15]) + float(player[15])) / 2 )
                                    csd10 = str(( float(line[16]) + float(player[16])) / 2 )
                                    cspm = str(( float(line[17]) + float(player[17])) / 2 )
                                    dpm = str(( float(line[19]) + float(player[19])) / 2 )
                                    egpm = str(( float(line[22]) + float(player[22])) / 2 )
                                    goldshare = str((float(line[23].split("%")[0])/100 + float(player[23].split("%")[0])/100)/2)
                                    wpm = str(( float(line[25]) + float(player[25])) / 2 )
                                    wcpm = str(( float(line[27]) + float(player[27])) / 2 )
                                    break
                        else:
                            kills = line[6]
                            deaths = line[7]
                            assists = line[8]
                            if line[10] == "":
                                kp = "0"
                            else:
                                kp = str(float(line[10].split("%")[0])/100)
                            if line[12] == "":
                                dth = "0"
                            else:
                                dth = str(float(line[12].split("%")[0])/100)
                            fb = str(float(line[13].split("%")[0])/100)
                            gd10 = line[14]
                            xpd10 = line[15]
                            csd10 = line[16]
                            cspm = line[17]
                            dpm = line[19]
                            egpm = line[22]
                            goldshare = str(float(line[23].split("%")[0])/100)
                            wpm = line[25]
                            wcpm = line[27]
                            
                        pred_row.append([kills,deaths,assists,kp,dth,fb,gd10,xpd10,csd10,cspm,dpm,egpm,goldshare,wpm,wcpm])
                        break
        pred_row.append([team1, team2])
        predict_in.append([item for sublist in pred_row for item in sublist])

    

    return predict_in


def double_in(data_in):
    final_in = []
    for match in data_in:
        single_match = []
        team1_data = match[0:75]
        team2_data = match[75:150]
        team1 = match[-2:][0]
        team2 = match[-2:][1]
        single_match.append(team1_data+team2_data)
        single_match.append(team2_data+team1_data)
        single_match.append(team1)
        single_match.append(team2)
        final_in.append(single_match)
    return final_in



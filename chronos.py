import csv
from tqdm import tqdm
import requests
import json
from datetime import datetime, timedelta
from os.path import exists

def get_start_dates():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'X-Api-Key': 'f561197a-82ea-4e54-acd2-386979018a7a',
    'Origin': 'https://oracleselixir.com',
    'Connection': 'keep-alive',
    'Referer': 'https://oracleselixir.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'If-None-Match': 'W/"40421-QNRN5iJt5cbdun6OMdXyEoQDMwc"',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    response = requests.get('https://oe.datalisk.io/tournaments/byLeague', headers=headers)
    return json.loads(response.text)

def get_correct_split(start_dates, league, year, match_date, t1_name):
    print(match_date)
    print(league)
    match_date = datetime.strptime(match_date, '%Y-%m-%d')
    return_start_date = "Failed to get league start date"
    target_split = league+str(year)
    if league == "ESLOL":
        league = "Elite Series"
    elif league == "LCK":
        league = "LCK/2022 Season"
    elif league == "LCS":
        league = "LCS/2022 Season"
    elif league == "LFL":
        league = "LFL/2022 Season"
    elif league == "VCS":
        league = "VCS/2022 Season"
    elif league == "LAS":
        league == "LCK Academy Series"
    elif league == "UL":
        league = "Ultraliga"
    elif league == "LFL2":
        league = "LFL Division 2"
    elif league == "HM":
        league = "Hitpoint Masters"
    elif league == "PGN":
        league = "PG Nationals"
    elif league == "LCSA":
        league = "NA Academy League"
    elif league == "LVP DDH":
        league = "División de Honor"
    elif league == "TRA":
        league = "Turkey Academy League"
    elif league == "CBLOLA":
        league = "Circuit Brazilian League of Legends Academy"
    elif league == "HC":
        league = "Hitpoint Challengers"
    elif league == "NEXO":
        league = "Liga Nexo"
    elif league == "GL":
        league = "Golden League"
    elif league == "SL":
        league = "LVP Superliga"
    elif league == "Proving Grounds Circuit" and match_date >= datetime.strptime("14/02/22 00:00:00", '%d/%m/%y %H:%M:%S') and t1_name in ["Dark Matter", "Glaive Esports Prime", "Trance's Tyrants"] and match_date >= datetime.strptime("16/02/22 23:59:00", '%d/%m/%y %H:%M:%S'):
        league =  "LCS Proving Grounds/2022 Season/Spring/Circuit Qualifier 2/Open Qualifier"
    elif league == "Proving Grounds Circuit" and match_date >= datetime.strptime("14/02/22 00:00:00", '%d/%m/%y %H:%M:%S') and match_date >= datetime.strptime("1/02/22 23:59:00", '%d/%m/%y %H:%M:%S'):
        league =  "LCS Proving Grounds/2022 Season/Spring/Open Qualifier 2"
    elif league == "Proving Grounds Circuit" and match_date <= datetime.strptime("12/01/22 00:00:00", '%d/%m/%y %H:%M:%S'):
        league =  "LCS Proving Grounds/2022 Season/Spring/Open Qualifier 1"
    for region in start_dates:
        for split in start_dates[region]:
            check_date = split["startDate"].split("T")[0]
            check_date = datetime.strptime(check_date, '%Y-%m-%d')
            if league == split["id"] or league == split["name"] or (league == split["fullName"] if "fullName" in split else False ) or (league == split["league"] if "league" in split else False ):
                if return_start_date == "Failed to get league start date" and check_date > datetime.strptime("01/12/21 00:00:00", '%d/%m/%y %H:%M:%S'):
                    return_start_date = check_date
                    target_split=split["id"]
                elif match_date >= check_date and abs(match_date - check_date) < abs(match_date - return_start_date) and check_date > datetime.strptime("01/12/21 00:00:00", '%d/%m/%y %H:%M:%S'): #return_start_date < match_date and return_start_date < check_date and match_date > check_date:
                    return_start_date = check_date
                    target_split=split["id"]
            elif league in split["name"] or league in split["id"]:
                if return_start_date == "Failed to get league start date" and check_date > datetime.strptime("01/12/21 00:00:00", '%d/%m/%y %H:%M:%S'):
                    return_start_date = check_date
                    target_split=split["id"]
                elif match_date >= check_date and check_date > datetime.strptime("01/12/21 00:00:00", '%d/%m/%y %H:%M:%S'): #return_start_date < #match_date and return_start_date < check_date and match_date > check_date:
                    return_start_date = check_date
                    target_split=split["id"]
    print(target_split)
    return [target_split,return_start_date]


def locate_past_data(split_season, split_start_date, split_end_date):
    url = ""
    if "Ultraliga" in split_season:
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+split_season.replace(" ", "%20").replace("/","%2F")+"&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    elif "ESLOL" in split_season:
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"Elite Series/2022 Season/Summer Split&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    elif "Mid-Season Invitational" in split_season:
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"2022 Mid-Season Invitational&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    elif "LCS Proving Grounds" in split_season and "Circuit" not in split_season:
        season = split_season.split("2022 Season/")[1].strip()
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"LCS Proving Grounds%2F2022 Season%2F" + season + "&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    elif "Liga Nexo" in split_season and "Relegations" in split_season:
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"Liga Nexo%2F2022 Season%2FRelegations&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    elif "CBLOL Academy/2022 Season/Split 1 Playoffs" in split_season:
        url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"CBLOL%20Academy%2F2022%20Season%2FSplit%201%20Playoffs&columnSet="
        filename = "./past_csvs/"+split_season.replace(" ", "%20").replace("/","%2F")+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
    else:
        part_1 = split_season.split("/")[0].replace(" ", "%20")
        #print(part_1)
        part_2 = split_season.split("/")[1].split(" ")[0]
        #print(part_2)
        part_3 = split_season.split("/")[1].split(" ")[1].split("/")[0]
        #print(part_3)
        part_4 = split_season.split("/")[2].split(" ")[0]
        #print(part_4)
        part_5 = split_season.split("/")[2]
        #print(part_5)
        if "Circuit" in part_5 and "Circuit Qualifier" not in part_5:
            part_5 = '%20'
        elif split_season == "LCS Proving Grounds/2022 Season/Spring":
            part_5 = "%2F" + part_5
        elif "Open Qualifier" in split_season or "Circuit Qualifier" in split_season:
            part_5 = '%2F'+split_season.split("/")[3].replace(" ", "%20")
        else:
            part_5 = '%20'+part_5.split(" ")[1].split("/")[0].strip()
        filename = "./past_csvs/"+part_1+part_2+part_3+part_4+part_5+split_start_date.strftime("%d-%m-%Y")+split_end_date+".csv"
        url = 'https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart='+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+'&tournament='+part_1+'%2F'+part_2+'%20'+part_3+'%2F'+ part_4 +part_5+'&columnSet'
    if exists(filename):
        pass
    else:
        print(url)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'X-Api-Key': 'f561197a-82ea-4e54-acd2-386979018a7a',
        'Origin': 'https://oracleselixir.com',
        'Connection': 'keep-alive',
        'Referer': 'https://oracleselixir.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'If-None-Match': 'W/"dc8-zMtYfllE7Aj7hL1aG8OLMOW7BJc"',
        }
        response = requests.get(url, headers=headers)
        if len(response.text) == 2:
            split_end_date = (datetime.strptime(split_end_date, '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")
            if "Ultraliga" in split_season:   
                url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+split_season.replace(" ", "%20").replace("/","%2F")+"&columnSet="
            elif "Liga Nexo" in split_season and "Relegations" in split_season:
                url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"Liga Nexo%2F2022 Season%2FRelegations&columnSet="
            elif "LCS Proving Grounds" in split_season and "Circuit" not in split_season:
                season = split_season.split("2022 Season/")[1].strip()
                url = "https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart="+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+"&tournament="+"LCS Proving Grounds%2F2022 Season%2F" + season + "&columnSet="   
            else:
                url = 'https://oe.datalisk.io/stats/teams/byTournament?mapSide=all&winLoss=all&dateStart='+split_start_date.strftime("%Y-%m-%d")+'&dateEnd='+split_end_date+'&tournament='+part_1+'%2F'+part_2+'%20'+part_3+'%2F'+ part_4 +part_5+'&columnSet'
        tdata = json.loads(response.text)
        csv_data = []
        for x in tdata:
            print(list(x.values())[1:])
            csv_data.append(list(x.values())[1:])
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
    return filename


def load_past_data(t1_row, t2_row, split_season, split_start_date, match_date):
    team1 = t1_row[17]
    team2 = t1_row[141]
    if team1 == "BT Excel": #Changed names
        team1 = "JD|XL"
    elif team1 == "Netshoes Miners":
        team1 = "Miners"
    elif team1 == "Netshoes Miners Academy":
        team1 = "Miners Academy"
    elif team1 == "Infinity Esports":
        team1 = "INFINITY"    

    if team2 == "BT Excel":
        team2 = "JD|XL"
    elif team2 == "Netshoes Miners":
        team2 = "Miners"
    elif team2 == "Netshoes Miners Academy":
        team2 = "Miners Academy"
    elif team2 == "Infinity Esports":
        team2 = "INFINITY"

    wint1 = t1_row[25]
    filename = locate_past_data(split_season, split_start_date, match_date)
    with open(filename, newline='') as f:
            reader = csv.reader(f)
            starting_data = list(reader)
    t1_stats = []
    t2_stats = []
    for row in starting_data:
        if row[0] == team1:
            t1_stats = row[1:]
        if row[0] == team2:
            t2_stats = row[1:]
    if t1_stats == []:
        print("Failed to find1 " + team1 + " in " + filename)
        exit()
    if t2_stats == []:
        print("Failed to find2 " + team2 + " in " + filename)
        exit()
    final_line = [wint1] + t1_stats + t2_stats
    return final_line





start_dates = get_start_dates()  
with open('all_data.csv', newline='') as f:
    reader = csv.reader(f)
    starting_data = list(reader)

only_team_data = []
for line in starting_data:
    if line[13] == "team":
        if line[56] != "":
            if line[115] != "":
                only_team_data.append(line)
#Add two teams data and write out the resulting amtches and results in all_out.csv
ready_all_data = []
first_part = True
for index, line in enumerate(only_team_data):
    if first_part:  #left right to result
        ready_all_data.append([line[25]] + line + only_team_data[index + 1])
        ready_all_data.append([line[25]] + only_team_data[index + 1] + line)  #add win of left team
        first_part = False
    else:
        first_part = True

final_data=[[
            "Team", "GP", "K", "D", "GL", "CKPM", "GPR", "GD15", "FB", "FT",
            "F3T", "PPG", "HLD", "FD", "DRG", "ELD", "BN", "FBN", "LNE", "JNG",
            "WPM", "CWPM", "WCPM"
        ]]
tmp_test = []

first_part = True
for index, row in enumerate(tqdm(ready_all_data)):
    if first_part:  #left right to result
        t1_row = row
        t2_row = [ready_all_data[index + 1]]
        t1_name = row[17]
        league = row[5]
        year = row[6]
        split = row[7]
        result = row[25]
        match_date = row[9].split(" ")[0]
        split_season, split_start_date = get_correct_split(start_dates, league, year, match_date,t1_name)
        #tmp_test.append(split_season + "  " +league)
        if type(split_start_date) == type("ok"):
            if "Failed to get league start date" in split_start_date:
                continue
        final_data.append(load_past_data(t1_row, t2_row ,split_season, split_start_date, match_date))
        first_part = False
    else:
        first_part = True

with open("test.csv", 'w', newline='') as csvfile:
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


with open("test_teams.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final_data)


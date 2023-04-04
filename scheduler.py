import wget
import glob
import os
import pytz
import time
from dateutil.parser import parse
from datetime import datetime, timezone
from icalendar import Calendar, Event, vDatetime
from lck_matches import get_lck_schedule

#Delete schedules
ical_files = glob.glob("*ical")
for file in ical_files:
    os.remove(file)

#Calendars with updated matches
lec_url = 'https://zlypher.github.io/lol-events/cal/league-of-legends-lec.ical'
lec_ical = wget.download(lec_url)
lcs_url = "https://zlypher.github.io/lol-events/cal/league-of-legends-lcs.ical"
lcs_ical = wget.download(lcs_url)
lck_url = "https://zlypher.github.io/lol-events/cal/league-of-legends-lck-champions-korea.ical"
lck_ical = wget.download(lck_url)

#Only for testing, you need to comment the deletion of schedules above if you want to use local/modified copies
#lec_ical = "./league-of-legends-lec.ical"
#lcs_ical = "./league-of-legends-lcs.ical"
#lck_ical = "./league-of-legends-lck-champions-korea.ical"



#worlds_url = "https://zlypher.github.io/lol-events/cal/league-of-legends-world-championship.ical"
#worlds_ical = wget.download(worlds_url)
#worlds_ical = "./league-of-legends-world-championship.ical"


'''
Gets the matches and teams and outputs them
if no matches exist, an empty list is returned
'''


def get_matches_today():
    all_matches = []
    for file in glob.glob("*ical"):
        region = ""
        if "lcs" in file:
            region = "LCS"
        elif "lec" in file:
            region = "LEC"
        elif "lck" in file:
            region = "LCK"
        elif "world" in file:
            region = "World Championship"
        g = open(file, 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                match = str(component.get('summary'))
                match_date = component.get('dtstart').dt
                all_matches.append([match_date, match,region])
        g.close()
    today = []
    for match in all_matches:
        print(match[1].split(" vs ")[0].strip() + " vs " + match[1].split(" vs ")[1].strip() + " at " + str(match[0].replace(tzinfo=pytz.utc)) + " and it is now " + str(datetime.now(timezone.utc)))
        if ((datetime.now(timezone.utc) - match[0].replace(tzinfo=pytz.utc)).total_seconds() < 0 and abs((datetime.now(timezone.utc) - match[0].replace(tzinfo=pytz.utc)).total_seconds()) < 85000): #Will run it at 06:00 CET, so all matches happening in the next 24, this way I get all of LCS
            if "bracket" in match[1] :
                team1 = match[1].split(": ")[1].split(" vs ")[0].strip()
                team2 = match[1].split(": ")[1].split(" vs ")[1].strip()
                today.append([team1, team2,"playoffs",match[2]])
            elif "Round 1" in match[1]:
                team1 = match[1].split(": ")[1].split(" vs ")[0].strip()
                team2 = match[1].split(": ")[1].split(" vs ")[1].strip()
                today.append([team1, team2])
            elif "Round" in match[1]:
                team1 = match[1].split(": ")[1].split(" vs ")[0].strip()
                team2 = match[1].split(": ")[1].split(" vs ")[1].strip()
                today.append([team1, team2,"playoffs",match[2]])
            elif "final" in match[1].lower() :
                team1 = match[1].split(": ")[1].split(" vs ")[0].strip()
                team2 = match[1].split(": ")[1].split(" vs ")[1].strip()
                today.append([team1, team2,"playoffs",match[2]])
            elif "Qualification match" in match[1] :
                team1 = match[1].split(": ")[1].split(" vs ")[0].strip()
                team2 = match[1].split(": ")[1].split(" vs ")[1].strip()
                today.append([team1, team2,"playoffs",match[2]])
            elif "TBD" in match[1]:
                continue
            else:
                team1 = match[1].split(" vs ")[0].strip()
                team2 = match[1].split(" vs ")[1].strip()
                today.append([team1, team2])
            print("Happening: " + team1 + " vs " + team2 + " with diff " + str((datetime.now(timezone.utc) - match[0].replace(tzinfo=pytz.utc)).total_seconds()))
            
    print("WE are thus predicting: ")
    print(today)
    return (today)



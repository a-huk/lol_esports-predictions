import wget
import glob
import os
from dateutil.parser import parse
from datetime import datetime
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

#lck will come at some point
'''
Gets the matches and teams and outputs them
if no matches exist, an empty list is returned
'''


def get_matches_today():
    all_matches = []
    with open(lec_ical, 'r') as file:
        data = file.read()

    for file in [lec_ical, lcs_ical]:
        g = open(file, 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                match = str(component.get('summary'))
                match_date = component.get('dtstart').dt
                all_matches.append([match_date, match])
        g.close()
    today = []
    for match in all_matches:
        if (abs((datetime.today() - match[0].replace(tzinfo=None)).total_seconds()) < 86400): #Will run it at 06:00 CET, so all matches happening in the next 24, this way I get all of LCS
            team1 = match[1].split(" vs ")[0].strip()
            team2 = match[1].split(" vs ")[1].strip()
            today.append([team1, team2])
    lck_matches = get_lck_schedule()
    for lck_match in lck_matches:
        today.append(lck_match)
    return (today)

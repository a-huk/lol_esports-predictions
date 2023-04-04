import datetime
import glob
import os
import time
import requests
import csv
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from selenium.webdriver.chrome.options import Options
import urllib.parse
'''
Obtain csv stats for a given region/split.
No API to obtain it, using selenium and headless firefox to obtain them.
Not to be abused.
league: "LEC" or "LCS" (for now)
return: path of the downloaded file
'''


def download_oe_data(content,league,season=False):

	#Change this when split change
	if season == False:
		if league == "LEC":
			season = "2023 Season/Winter Season"
		elif league == "LCS":
			#season = "2023 Season/Spring Season"
			season = "2023 Season/Spring Playoffs"
		elif league == "LCK":
			#season = "2023 Season/Spring Season"
			season = "2023 Season/Spring Playoffs"
		else:
			print("ERROR: You need to specify a season or the provided league does not have a pre-determined season stored in get_team_stats.py")
			exit()
	print("downloading")
	print(season)
	print(league)
	season = urllib.parse.quote(season)
	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Api-Key': 'f561197a-82ea-4e54-acd2-386979018a7a',
    'Origin': 'https://oracleselixir.com',
    'Connection': 'keep-alive',
    'Referer': 'https://oracleselixir.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
	}
	response = requests.get('https://oe.datalisk.io/stats/' + content + '/byTournament?mapSide=all&winLoss=all&tournament=' + league + '%2F' + season + '&columnSet', headers=headers)
	filename = league + str(date.today().year) + season + content
	filename = filename.replace("","").replace("/","")
	return response2csv(response.text,filename)
	
	#OLD version using webdriver, direct requests are much more interesting
	"""

	if league == "LCS":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCS%2F2022%20Season%2FSummer " + season
	elif league == "LEC":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LEC%2F2022%20Season%2FSummer " + season
	elif league == "LCK":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCK%2F2022%20Season%2FSummer " + season
	elif league == "VCS":
		url = "https://oracleselixir.com/stats/" + content + "byTournament/VCS%2F2022%20Season%2FSummer%20Playoffs"
	elif league == "LLA":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LLA%2F2022%20Season%2FSummer " + season
	elif league == "LJL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LJL%2F2022%20Season%2FSummer " + season
	elif league == "LCO":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCO%2F2022%20Season%2FSplit 1 Playoffs"
	elif league == "TCL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/TCL%2F2022%20Season%2FWinter Playoffs"
	elif league == "LPL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LPL%2F2022%20Season%2FSummer " + season
	elif league == "CBLOL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/CBLOL%2F2022%20Season%2FSplit 1 Playoffs"
	elif league == "PCS":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/PCS%2F2022%20Season%2FSummer " + season
	elif league == "World Championship":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/2022%20Season%20World%20Championship%2FMain%20Event"
		print("This")
	
	print(url)
	fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList", 2)
	opt = webdriver.FirefoxOptions()
	opt.add_argument('-headless')
	downloads_dir = str(Path.home() / "Downloads")
	fp.set_preference("browser.download.dir", downloads_dir)
	fp.set_preference("browser.download.manager.showWhenStarting", False)
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
	print("beforrrr")
	browser = webdriver.Firefox(firefox_profile=fp, options=opt)
	browser.set_page_load_timeout(30)
	print("beforrrr2")
	browser.get(url)
	time.sleep(1)
	print("beforrrr3")
	browser.get(url)
	print("afterrrrr")
	time.sleep(10)
	if "Unable to fetch tournament with this ID" in browser.find_element_by_tag_name("body").get_attribute("innerText") :
		print("inside unable")
		browser.quit()
		return "nothing"
	else:
		elems = browser.find_elements_by_xpath("//a")
		for elem in elems:
			if "Download This Table" in elem.text:
				elem.click()
				list_of_files = glob.glob(downloads_dir + "/*"+ league +"*")
				if league == "World Championship":
					list_of_files = glob.glob(downloads_dir + "/*"+ "Worlds" +"*.csv")
				latest_file = max(list_of_files, key=os.path.getctime)
				browser.quit()
				print("Done")
				return latest_file
	"""

def download_custom_oe_data(content,league,season, cStart, cEnd): #Not updated
	print("downloading")
	print(season)
	print(league)
	print(content)
	"""headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
	'Accept': '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	# 'Accept-Encoding': 'gzip, deflate, br',
	'X-Api-Key': 'f561197a-82ea-4e54-acd2-386979018a7a',
	'Origin': 'https://oracleselixir.com',
	'Connection': 'keep-alive',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'no-cors',
	'Sec-Fetch-Site': 'cross-site',
	'If-None-Match': 'W/"dbd-S0zXEGTU+3XOMEclop7QlyiJGJI"',
	# Requests doesn't support trailers
	# 'TE': 'trailers',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Referer': 'https://oracleselixir.com/',
}

	response = requests.get('https://oe.datalisk.io/stats/'+content+'/byTournament?mapSide=all&winLoss=all&dateStart=2021-06-17&dateEnd=2022-06-19&tournament='+league+'%2F2022%20Season%2FSummer%20'+season+'&columnSet', headers=headers)

	filename = league + str(date.today().year) + season + content
	return response2csv(response.text,filename)"""
	url =""
	if league == "LCS":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCS%2F2022%20Season%2FSummer " + season
	elif league == "LEC":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LEC%2F2022%20Season%2FSummer " + season
	elif league == "LCK":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCK%2F2022%20Season%2FSummer " + season
	elif league == "VCS":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/VCS%2F2022%20Season%2FSummer " + season
	elif league == "LLA":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LLA%2F2022%20Season%2FSummer " + season
	elif league == "LJL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LJL%2F2022%20Season%2FSummer " + season
	elif league == "LCO":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCO%2F2022%20Season%2FSplit 1 Playoffs"
	elif league == "TCL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/TCL%2F2022%20Season%2FWinter Playoffs"
	elif league == "LPL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LPL%2F2022%20Season%2FSummer " + season
	elif league == "CBLOL":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/CBLOL%2F2022%20Season%2FSplit 1 Playoffs"
	elif league == "PCS":
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/PCS%2F2022%20Season%2FSummer " + season
	elif league == "World Championship":
		#url = "https://oracleselixir.com/stats/" + content + "/byTournament/2022%20Season%20World%20Championship%2FMain%20Event"
		url = "https://oracleselixir.com/stats/" + content + "/byTournament/LCO%2F2022%20Season%2FSplit 1 Playoffs"
	print(url)

	fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList", 2)
	opt = webdriver.FirefoxOptions()
	opt.add_argument('-headless')
	downloads_dir = str(Path.home() / "Downloads")
	fp.set_preference("browser.download.dir", downloads_dir)
	fp.set_preference("browser.download.manager.showWhenStarting", False)
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
	browser = webdriver.Firefox(firefox_profile=fp, options=opt)
	browser.get(url)
	browser.get(url)
	time.sleep(10)
	if "Unable to fetch tournament with this ID" in browser.find_element_by_tag_name("body").get_attribute("innerText") :
		browser.quit()
		return "nothing"
	else:
		start_date = browser.find_element_by_id("start_date")
		time.sleep(1)
		start_date.clear()
		time.sleep(1)
		start_date.send_keys(cStart)
		time.sleep(1)
		end_date = browser.find_element_by_id("end_date")
		time.sleep(1)
		end_date.clear()
		time.sleep(1)
		end_date.send_keys(cEnd)
		time.sleep(8)
		elems = browser.find_elements_by_xpath("//a")
		for elem in elems:
			if "Download This Table" in elem.text:
				elem.click()
		list_of_files = glob.glob(downloads_dir + "/*"+ league +"*")
		latest_file = max(list_of_files, key=os.path.getctime)
		browser.quit()


def response2csv(response, name):
	csv_list = []
	jdata = json.loads(response)
	csv_list.append(list(jdata[0].keys())[1:])
	for team in jdata:
		print(team)
		csv_list.append(list(team.values())[1:])

	filename = '/root/Downloads/'+name+'.csv'
	if os.path.exists(filename):
		os.remove(filename)
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(csv_list)
	return filename


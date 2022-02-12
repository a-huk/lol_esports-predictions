import datetime
import glob
import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
'''
Obtain csv stats for a given region/split.
No API to obtain it, using selenium and headless firefox to obtain them.
Not to be abused.
league: "LEC" or "LCS" (for now)
return: path of the downloaded file
'''


def download_week(league):
    if league == "LCS":
        url = "https://oracleselixir.com/stats/teams/byTournament/LCS%2F2022%20Season%2FSpring%20Season"
    elif league == "LEC":
        url = "https://oracleselixir.com/stats/teams/byTournament/LEC%2F2022%20Season%2FSpring%20Season"
    elif league == "LCK":
        url = "https://oracleselixir.com/stats/teams/byTournament/LCK%2F2022%20Season%2FSpring%20Season"

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
    time.sleep(3)
    elems = browser.find_elements_by_xpath("//a")
    for elem in elems:
        if "Download This Table" in elem.text:
            elem.click()
    list_of_files = glob.glob(downloads_dir + "/*")
    latest_file = max(list_of_files, key=os.path.getctime)
    browser.quit()
    return latest_file

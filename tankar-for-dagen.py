#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import episode as episode_util

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=sv')
  
prefs = {"profile.default_content_setting_values.notifications": 2} 
chrome_options.add_experimental_option("prefs", prefs) 
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options) 

show_more_url='https://sverigesradio.se/tankarfordagen/sida/episode/showmoreepisodelistitems?unitid=1165&page={PAGE}&ajax=true&gaaction=click&gakey=avsnittslista_visa_fler_senaste&gatrackcontext=avsnittslista&date=' + episode_util.today() + '%2000:00:00'

def show_more(driver, page):
    url = show_more_url.replace('{PAGE}', str(page))
    driver.get(url)
    time.sleep(1)

def show_all_episodes(driver):
    try:
        while True:
            show_more(driver)
    except NoSuchElementException:
        return

# Main 'loop'
driver.get('https://sverigesradio.se/tankarfordagen')
try:
    page = 0
    while True:
        print('Page: ' + str(page))
        episodes = episode_util.get_episodes(driver)
        print('Episode count: ' + str(len(episodes)))

        for episode in episodes:
            episode.download()
        
        show_more(driver, page)
        page += 1
except NoSuchElementException:
    print('Downloaded all episodes')

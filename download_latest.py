#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import episode as episode_util

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=sv')
  
prefs = {"profile.default_content_setting_values.notifications": 2} 
chrome_options.add_experimental_option("prefs", prefs) 
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options) 

# Helgsmål
print('Downloading helgsmål')
download_link='https://lyssna-cdn.sr.se/ljudit/p1/helgsmal/{YEAR}/{MONTH}/helgsmal_{YEAR}{MONTH}{DAY}_1800_192.m4a'

driver.get('https://sverigesradio.se/helgsmal')
episodes = episode_util.get_episodes(driver)
for episode in episodes:
    # Set download url for Helgsmål
    date_split = episode.date.split('-')
    year = date_split[0]
    month = date_split[1]
    day = date_split[2]
    episode.url = download_link.replace('{YEAR}', year)
    episode.url = episode.url.replace('{MONTH}', month)
    episode.url = episode.url.replace('{DAY}', day)
    episode.dir = 'Helgsmål'
    episode.download()


# Tankar för dagen
print('Downloading tankar för dagen')
driver.get('https://sverigesradio.se/tankarfordagen')
episodes = episode_util.get_episodes(driver)
for episode in episodes:
    episode.dir = 'Tankar för dagen'
    episode.download()

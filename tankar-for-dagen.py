#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import urllib.request
import os.path
from datetime import date, timedelta

def print_raw(text):
    text = text + '\n'
    sys.stdout.buffer.write(text.encode('utf8'))

month_to_number = {
    'jan': '01',
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'maj': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'okt': '10',
    'nov': '11',
    'dec': '12',
}


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=sv')
  
prefs = {"profile.default_content_setting_values.notifications": 2} 
chrome_options.add_experimental_option("prefs", prefs) 
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options) 


def today():
    return date.today().strftime('%Y-%m-%d')

def yesterday():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def this_year():
    return date.today().strftime('%Y')

def get_date_from_episode(episode):
    date_text = episode.find_elements_by_class_name('metadata-item-text')[1].text
    split_date = date_text.split(' ')

    # Today
    if len(split_date) == 2:
        return today()
    # Yesterday
    elif len(split_date) == 3:
        return yesterday()
    # This year
    elif len(split_date) == 5:
        date = this_year() + '-'
        date += month_to_number[split_date[2]] + '-'
        date += split_date[1]
        return date
    else:
        date = split_date[3] + '-'
        date += month_to_number[split_date[2]] + '-'
        date += split_date[1]
        return date

show_more_url='https://sverigesradio.se/tankarfordagen/sida/episode/showmoreepisodelistitems?unitid=1165&page={PAGE}&ajax=true&gaaction=click&gakey=avsnittslista_visa_fler_senaste&gatrackcontext=avsnittslista&date=' + today() + '%2000:00:00'

def show_more(driver, page):
    url = show_more_url.replace('{PAGE}', str(page))
    driver.get(url)
#     show_more = driver.find_element_by_xpath('//button[@data-bt-type="js-show-more"]')
#     print(show_more.toString())
#     driver.execute_script('arguments[0].scrollIntoView(true)', show_more)
#     show_more.click()
    time.sleep(1)

def show_all_episodes(driver):
    try:
        while True:
            show_more(driver)
    except NoSuchElementException:
        return

def download_episode(episode):
        title = episode.find_element_by_class_name('heading').text
        episode_date = get_date_from_episode(episode)
        file_name = episode_date + ' ' + title + '.mp3'

        # Only download new files
        if not os.path.exists(file_name):
            print('Downloading: ' + file_name)
            download_link = episode.find_element_by_xpath('.//a[contains(@href,"mp3")]').get_attribute('href')
            urllib.request.urlretrieve(download_link, file_name)
        else:
            print('Skipping: ' + file_name)

# Main 'loop'
driver.get('https://sverigesradio.se/tankarfordagen')
try:
    page = 0
    while True:
        print('Page: ' + str(page))
        episodes = driver.find_elements_by_class_name('episode-list-item')
        print('Episode count: ' + str(len(episodes)))

        for episode in episodes:
            download_episode(episode)
        
        show_more(driver, page)
        page += 1
except NoSuchElementException:
    print('Downloaded all episodes')

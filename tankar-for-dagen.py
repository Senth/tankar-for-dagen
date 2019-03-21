#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import urllib.request
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

driver.get('https://sverigesradio.se/tankarfordagen')

print(sys.getfilesystemencoding())

def show_all_episodes(driver):
    try:
        while True:
            show_more = driver.find_element_by_xpath('//button[@data-bt-type="js-show-more"]')
            show_more.click()
            time.sleep(2)
    except NoSuchElementException:
        return

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


show_all_episodes(driver)
episodes = driver.find_elements_by_class_name('episode-list-item')

for episode in episodes:
    title = episode.find_element_by_class_name('heading').text

    episode_date = get_date_from_episode(episode)

    download_link = episode.find_element_by_xpath('.//a[contains(@href,"mp3")]').get_attribute('href')

    file_name = episode_date + ' ' + title + '.mp3'
    print_raw('file_name: ' + file_name)

    urllib.request.urlretrieve(download_link, file_name)

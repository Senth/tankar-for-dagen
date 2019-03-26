from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
import urllib.request
import os.path
from os import mkdir

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

def today():
    return date.today().strftime('%Y-%m-%d')

def yesterday():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def this_year():
    return date.today().strftime('%Y')

def get_date(episode_element):
    date_text = episode_element.find_elements_by_class_name('metadata-item-text')[1].text
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

def get_episodes(driver):
    episode_elements = driver.find_elements_by_class_name('episode-list-item')
    episodes = list()

    for episode_element in episode_elements:
        episode = Episode(episode_element)
        episodes.append(episode)

    return episodes


class Episode:
    def __init__(self, episode_element):
        self.title = episode_element.find_element_by_class_name('heading').text
        # Remove question mark
        self.title = self.title.replace('?', '')

        self.date = get_date(episode_element)
        self.dir = ''
        self.file = self.date + ' ' + self.title
        self.ext = 'mp3'

        try:
            self.url = episode_element.find_element_by_xpath('.//a[contains(@href,"mp3")]').get_attribute('href')
        except NoSuchElementException:
            self.url = ''
            self.ext = 'm4a'

    def filename(self):
        if len(self.dir) > 0:
            return os.path.join(self.dir,self.file + '.' + self.ext)
        else:
            return self.file + '.' + self.ext

    def download(self):
        # Create dir
        if not os.path.exists(self.dir):
            mkdir(self.dir)

        # Only download new files
        if not os.path.exists(self.filename()):
            print('Downloading: ' + self.filename() + ' (' + self.url + ')')
            urllib.request.urlretrieve(self.url, self.filename())
        else:
            print('Skipping: ' + self.filename())
        

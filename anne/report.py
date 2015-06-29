from urllib.request import urlretrieve
from os.path import getmtime, isfile
from time import time
import xml.etree.ElementTree as etree

from anne.anime import Anime


DAY = 60*60*24

class Report:
    url = "http://www.animenewsnetwork.com/encyclopedia/reports.xml?id=155&type=anime&nlist=all"
    filename = ''
    contents = ''

    def __init__(self, filename='report.xml'):
        self.filename = filename

    def __report_exists(self):
        return isfile(self.filename)

    # returns true if the report is less than a day old
    def __report_is_valid(self):
        if self.__report_exists():
            return getmtime(self.filename) > time() - DAY
        return False

    def __download_report(self):
        if not self.__report_is_valid():
            urlretrieve(self.url, self.filename)

    def __read_report_contents(self):
        with open(self.filename, 'r') as f:
            self.contents = f.read()
        return self.contents

    def get_report(self):
        self.__download_report()
        return self.__read_report_contents()

    def get_report_as_et(self):
        self.__download_report()
        return etree.parse(self.filename)
    
    def get_all_anime(self):
        root = self.get_report_as_et().getroot()
        items = root.findall('item')
        return [Anime(item.find('id').text, item.find('name').text) for item in items]


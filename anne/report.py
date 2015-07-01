import xml.etree.ElementTree as etree

from anne.anime import Anime
from anne.request import get


class Report:
    url = "http://www.animenewsnetwork.com/encyclopedia/reports.xml?id=155&type=anime&nlist=all"
    contents = ''

    def get_report(self):
        if not self.contents:
            self.contents = get(self.url)
        return self.contents

    def get_report_as_et(self):
        self.get_report()
        return etree.fromstring(self.contents)
    
    def get_all_anime(self):
        root = self.get_report_as_et()
        items = root.findall('item')
        return [Anime(item.find('id').text, item.find('name').text) for item in items]


import xml.etree.ElementTree as etree
from difflib import get_close_matches
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
        anime = [Anime(item.find('id').text, item.find('name').text) for item in items]
        return { a.name: a for a in anime }

    def search(self, term):
        anime = self.get_all_anime()
        titles = get_close_matches(term, list(anime.keys()), 5)
        return [anime[title] for title in titles]


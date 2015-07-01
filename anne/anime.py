import xml.etree.ElementTree as etree
from anne.request import get 


class Anime:
    base_url = "http://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime={}"

    def __init__(self, anne_id, name):
        self.anne_id = anne_id
        self.name = name

    def __get_data(self):
        url = self.base_url.format(self.anne_id)
        self.response = get(url)

    def __parse_info(self):
        root = etree.fromstring(self.response).find('anime')
        info = {}
        for item in root.findall('info'):
            atype = item.attrib['type']
            info[atype] = info.get(atype, [])
            info[atype].append(item.text)
        self.info = info

    def __parse_episodes(self):
        root = etree.fromstring(self.response).find('anime')
        episodes = {}
        for episode in root.findall('episode'):
            episodes[episode.attrib['num']] = episode.find('title').text
        self.episodes = episodes

    def __parse_response(self):
        self.__parse_info()
        self.__parse_episodes()

    def fill(self):
        self.__get_data()
        self.__parse_response()
        del self.response

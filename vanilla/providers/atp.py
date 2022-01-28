import sys,os
from extract.website import Website
from providers.provider import Provider

class Atp(Provider):

    def __init__(self):
        super().__init__()
        self.name = "ATP"
        self.url = "https://www.atptour.com/"

    def get_top_players_links(self, n:int=None):
        """[retreive urls to the atp profile page for the top n players]

        :param [n]: [number of players], defaults to [None]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [urls]
        :rtype: [list]
        """
        web = Website(url="https://www.atptour.com/en/rankings/singles")
        links = web.get_links()
        player_links = [ str(_) for _ in links if "/en/players/" in str(_) and 'overview' in str(_) ] # two links per player are displayed (1) overivew, (2)rankings breakdown
        if n != None:
            player_links = player_links[:n]
        urls = [self.url + _ for _ in player_links]
        return urls


    def extract_player_id_from_url(self, urls:list):
        """[extract player id from url]

        :param [url]: [url to player profile page]
        ...
        :return: [d]
        :rtype: [dictionary]
        """
        def parse(url:str):
            splits = url.split('/')
            name, id = splits[6], splits[7]
            return (name, id)

        dict = {}
        if isinstance(urls, list):
            for url in urls:
                name, id = parse(url)
                dict[id] = name

        elif isinstance(urls, str):
            name, id = parse(urls)
            dict[id] = name

        return dict
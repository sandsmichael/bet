
   
import sys,os
import pandas as pd
from extract.website import Website
from providers.atp.atp import Atp

class Rankings(Atp):

    def __init__(self):
        super().__init__()
        self.name = "ATP_Rankings"
        self.url = "https://www.atptour.com/en/rankings/singles"
 
    def get_top_players_links(self, n:int=None):
        """[retreive urls to the atp profile page for the top n players]

        :param [n]: [number of players], defaults to [None]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [links]
        :rtype: [list]
        """
        web = Website(url=self.url)
        links = web.get_links()
        player_links = [ str(_) for _ in links if "/en/players/" in str(_) and 'overview' in str(_) ] # two links per player are displayed (1) overivew, (2)rankings breakdown
        if n != None:
            player_links = player_links[:n]
        links = [self.atp_url + _ for _ in player_links]
        return links


    def extract_player_id_from_url(self, links:list):
        """[extract player id from url]

        :param [url]: [url to player profile page]
        ...
        :return: [df]
        :rtype: [dataframe]
        """
        def parse(link:str):
            splits = link.split('/')
            name, id = splits[6], splits[7]
            return (name, id)

        dict = {}
        if isinstance(links, list):
            for link in links:
                name, id = parse(link)
                dict[id] = name

        elif isinstance(links, str):
            name, id = parse(links)
            dict[id] = name

        df = pd.DataFrame.from_dict(dict, orient='index').reset_index().rename(columns={0:'name'})
        df[['first', 'last']] = df.name.str.rsplit('-', 1, expand=True) # NOTE: split from right maxsplit=1 in case hyphenated player name
        df.rename(columns={'index':'id'}, inplace=True)
        return df


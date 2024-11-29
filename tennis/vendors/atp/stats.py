import sys,os
import pandas as pd
from extract.website import Website
from vendors.atp.player import Player

basedir = os.path.dirname(os.path.abspath(__file__))


class Stats(Player):

    def __init__(self, last_name:str = None, year:str = None, surface:str = None):
        """[retreive stats for a plyer from atp pllayer stats page]

        :param [lastname]: [player last name as stored in atp_player_ids.csv scrape], defaults to [None]
        :param [year]: [year for stats period], defaults to [None]
            "career" == 0 else YYYY
        :param [surface]: [surface for stats period], defaults to [None]
            "all surfaces" == "all" else "hard", "clay", "grass", "carpet"
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [links]
        :rtype: [list]
        """
        super().__init__(last_name)
        self.last_name = last_name
        self.year = year
        self.surface = surface
        self.name = "ATP_Player_Stats"

    
    def get_player_url(self):
        player_row = self.get_player_id_row()
        url = self.player_url + player_row.name.values[0] + '/'+ player_row.id.values[0] + '/' + f'player-stats?year={self.year}&surfaceType={self.surface}'
        return url


    def get_stats_serve(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return web.scrape_table_to_df(attrb='id', value='playerMatchFactsContainer')[0]

    def get_stats_return(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return web.scrape_table_to_df(attrb='id', value='playerMatchFactsContainer')[1]

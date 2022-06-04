import sys,os
import pandas as pd
from extract.website import Website
from vendors.atp.player import Player

basedir = os.path.dirname(os.path.abspath(__file__))

class Activity(Player):

    def __init__(self, last_name:str = None, year:str = None, surface:str = None):
        """

        :param [lastname]: [player last name as stored in atp_player_ids.csv scrape], defaults to [None]

        :raises [ErrorType]: [ErrorDescription]

        :return: [links]
        :rtype: [list]
        """
        super().__init__(last_name)
        self.last_name = last_name
        self.year = year
        self.surface = surface
        self.name = "ATP_Player_Activity"
    
    def get_player_url(self):
        player_row = self.get_player_id_row()
        url = self.player_url + player_row.name.values[0] + '/'+ player_row.id.values[0] + '/' + 'player-activity'
        return url

    def get(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return web.scrape_table_to_df(elm = 'div', attrb='class', value='activity-tournament-table')


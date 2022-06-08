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
        url = self.player_url + player_row.name.values[0] + '/'+ player_row.id.values[0] + '/' + f'player-activity?year={self.year}'
        return url

    def get(self):
        '''
        each tournament is represented in three separate tables (1) for tournament name header, (2) for prize money and (3) for match results
        i.e. table index 0 has table name, and index 2 has results...or 3 has table_name and 5 has results. itterate by two.
            act = Activity(last_name = 'nadal', year='2022')
            df_act = act.get()
            n = len(df_act)
            for i in range(0, n, 3):
                df = df_act[i+2]
                df['tournament'] = df_act[i][1].iloc[0]
        '''
        web = Website(url = self.get_player_url())
        web.scrape()
        return web.scrape_table_to_df(elm = 'div', attrb='class', value='activity-tournament-table')



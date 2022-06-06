import sys,os
import pandas as pd
from extract.website import Website
from vendors.atp.player import Player

basedir = os.path.dirname(os.path.abspath(__file__))

class WinLoss(Player):

    def __init__(self, last_name:str = None):
        """ [lastname]: [player last name as stored in atp_player_ids.csv scrape], defaults to [None]
        """
        super().__init__(last_name)
        self.last_name = last_name

    def set_columns(self, df):
        df.columns = ['index', 'ytd', 'ytd pct', 'career', 'career pct','titles']
        return df

    def get_player_url(self):
        player_row = self.get_player_id_row()
        url = self.player_url + player_row.name.values[0] + '/'+ player_row.id.values[0] + '/' + 'fedex-atp-win-loss'
        return url

    def get_overall(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return self.set_columns(web.scrape_table_to_df(attrb='id', value='matchRecordWrapper')[0].dropna())

    def get_pressure(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        df =  self.set_columns(web.scrape_table_to_df(attrb='id', value='matchRecordWrapper')[7])
        df.drop('titles', axis=1, inplace=True)
        df.dropna(inplace = True)
        return df

    def get_environment(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return self.set_columns(web.scrape_table_to_df(attrb='id', value='matchRecordWrapper')[18].dropna())

    def get_other(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        df =  self.set_columns(web.scrape_table_to_df(attrb='id', value='matchRecordWrapper')[31])
        df.drop('titles', axis=1, inplace=True)
        df.dropna(inplace = True)
        return df

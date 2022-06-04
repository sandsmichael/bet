import sys,os
import pandas as pd
from extract.website import Website
from vendors.atp.player import Player

basedir = os.path.dirname(os.path.abspath(__file__))

class WinLoss(Player):

    def __init__(self, last_name:str = None):
        """

        :param [lastname]: [player last name as stored in atp_player_ids.csv scrape], defaults to [None]
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [links]
        :rtype: [list]
        """
        super().__init__(last_name)
        self.last_name = last_name

    def get_player_url(self):
        player_row = self.get_player_id_row()
        url = self.player_url + player_row.name.values[0] + '/'+ player_row.id.values[0] + '/' + 'fedex-atp-win-loss'
        return url

    def get(self):
        web = Website(url = self.get_player_url())
        web.scrape()
        return web.scrape_table_to_df(attrb='id', value='matchRecordWrapper')[0]


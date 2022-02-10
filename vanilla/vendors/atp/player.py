import sys,os
import pandas as pd
from extract.website import Website
from vendors.atp.atp import Atp

basedir = os.path.dirname(os.path.abspath(__file__))

class Player(Atp):

    def __init__(self, last_name:str = None):
        super().__init__()
        self.last_name = last_name
        self.name = "ATP_Rankings"
        self.player_url = "https://www.atptour.com/en/players/"
        self.fp_player_ids = os.path.join(os.path.dirname(os.path.dirname(basedir)), 'io/out/atp_player_ids.csv')

    
    def get_player_id_row(self):
        df = pd.read_csv(self.fp_player_ids)
        player_row = df.loc[df['last'] == self.last_name]
        assert len(player_row==1), '[ERROR] more than one player with last_name key found in player ids'
        return player_row


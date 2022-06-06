import pandas as pd

from vendors.atp.stats import Stats
from vendors.atp.winloss import WinLoss
from vendors.atp.activity import Activity

class Match:
    
    ''' p1 = player 1 last name; p2 = player 2 last name
    '''

    def __init__(self, p1_lname:str, p2_lname:str):
        self.p1_lname = p1_lname
        self.p2_lname = p2_lname
        
    def build_serve_return_frame(self):
        year, surface = '2022', 'clay'
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            stats = Stats(last_name = p,  year=year, surface=surface)
            df_serve = stats.get_stats_serve().rename(columns={'Singles Service Record': 'metric', 'Singles Service Record.1':'value'})
            df_return = stats.get_stats_return().rename(columns={'Singles Return Record': 'metric', 'Singles Return Record.1':'value'})
            df = pd.concat([df_serve, df_return], axis=0, ignore_index=True)
            df.rename(columns={'value':p}, inplace=True)
            frames.append(df)
        df = pd.concat(frames, axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        df.set_index('metric', inplace=True)
        print(df)        
        return df


    def build_win_loss_frame(self):
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            wl = WinLoss(last_name = p)
            player_frames = [ wl.get_overall(), wl.get_pressure(), wl.get_environment(), wl.get_other() ]
            df = pd.concat(player_frames, axis=0, ignore_index=True)
            df.columns = ['index'] + [f'{p}_{c}' for c in df.columns if c != 'index']
            frames.append(df)
        df = pd.concat(frames, axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        df.set_index('index', inplace=True)
        print(df)
        return df


    def build_activity_frame(self):
        act = Activity(last_name = 'nadal', year='2022')
        df_act = act.get()
        n = len(df_act)
        frames = []
        for i in range(0, n, 3):
            df = df_act[i+2]
            df['tournament'] = df_act[i][1].iloc[0]
            frames.append(df)
        df = pd.concat(frames, axis=0, ignore_index=True)
        print(df)

m = Match('nadal', 'ruud')
m.build_serve_return_frame()
m.build_win_loss_frame()
m.build_activity_frame()
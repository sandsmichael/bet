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
        # print(df)        
        return df


    def build_win_loss_frame(self):
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            wl = WinLoss(last_name = p)
            player_frames = [ wl.get_overall(), wl.get_pressure(), wl.get_environment(), wl.get_other() ]
            df = pd.concat(player_frames, axis=0, ignore_index=True)
            df.columns = ['index'] + [f'{p}_{c}' for c in df.columns if c != 'index']

            split_list = ['_ytd', '_career']
            for s in split_list:
                label = f'{p}{s}'
                new_label_win = f'{p}{s} win'
                new_label_loss = f'{p}{s} loss'
                df[[new_label_win, new_label_loss]] = df[label].str.split('-', 1, expand=True)
                df.drop(label, axis=1, inplace=True)
            
            for c in df.columns:
                try:
                    df[c] = pd.to_numeric(df[c] )
                except:
                    pass
            
            cols = ['index'] + [p + c for c in ['_ytd pct','_ytd win','_ytd loss','_career pct','_career win','_career loss','_titles']]
            df = df[cols]

            frames.append(df)
        df = pd.concat(frames, axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        df.set_index('index', inplace=True)
        # print(df)
        return df


    def build_activity_frame(self):
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            act = Activity(last_name = self.p1_lname, year='2022')
            df_act = act.get()
            n = len(df_act)
            tourny_frames = []
            for i in range(0, n, 3):
                df = df_act[i+2]
                df['tournament'] = df_act[i][1].iloc[0]
                tourny_frames.append(df)
            df = pd.concat(tourny_frames, axis=0, ignore_index=True)
            frames.append(df)
        return frames[0], frames[1]



    def build_prediction_frame(self) -> pd.DataFrame:
        ''' build a match stats frame with features of both players for match result prediction
        features:
            'p1_hand', 'p1_rank','p1_ht', 'p1_ace','p1_svpt', 'p1_1stIn', 'p1_1stWon', 'p1_2ndWon', 'p1_SvGms', 'p1_bpSaved', 'p1_bpFaced', 
            'p2_hand','p2_rank', 'p2_ht', 'p2_ace', 'p2_svpt', 'p2_1stIn', 'p2_1stWon', 'p2_2ndWon', 'p2_SvGms', 'p2_bpSaved', 'p2_bpFaced'
        '''
        pass




# m = Match('nadal', 'ruud')
# m.build_serve_return_frame()
# m.build_win_loss_frame()
# m.build_activity_frame()
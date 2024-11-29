import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vendors.atp.stats import Stats
from vendors.atp.winloss import WinLoss
from vendors.atp.activity import Activity
from datetime import timedelta

class Match:

    ''' p1 = player 1 last name; p2 = player 2 last name
    '''

    def __init__(self, p1_lname:str, p2_lname:str, surface='hard', year = 'clay'):
        self.p1_lname = p1_lname
        self.p2_lname = p2_lname
        self.surface = surface
        self.year = year
        

    def build_serve_return_frame(self):
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            stats = Stats(last_name = p,  year=self.year, surface=self.surface)
            df_serve = stats.get_stats_serve().rename(columns={'Singles Service Record': 'metric', 'Singles Service Record.1':'value'})
            df_return = stats.get_stats_return().rename(columns={'Singles Return Record': 'metric', 'Singles Return Record.1':'value'})
            df = pd.concat([df_serve, df_return], axis=0, ignore_index=True)
            df.rename(columns={'value':p}, inplace=True)
            frames.append(df)
        df = pd.concat(frames, axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        df.set_index('metric', inplace=True)
        self.sr = df
        return df


    def split_by_type(self):
        sr_fmt = self.sr.copy()
        sr_unfmt = pd.DataFrame()
        for c in sr_fmt.columns:
            for i in range(len(sr_fmt[c])):
                if '%' in sr_fmt[c].iloc[i]:
                    sr_fmt[c].iloc[i] = int(str(sr_fmt[c].iloc[i]).replace('%',''))/100
                    
            sr_fmt[c] = pd.to_numeric(sr_fmt[c])
            
            sr_unfmt[c]  = sr_fmt[c]
            sr_unfmt[c] = sr_unfmt[c][(sr_unfmt[c] > 1)] 

            sr_fmt[c] = sr_fmt[c][~(sr_fmt[c] > 1)] 
        
        self.sr_percent = sr_fmt.dropna( axis=0)
        self.sr_absolute = sr_unfmt.dropna( axis=0)
        

    def spider_plot(self, sr):
        feats = ['Service Games Won','Total Service Points Won', 'Return Games Won', 'Return Points Won', 'Break Points Converted']
        _sr = sr.copy()
        for c in _sr.columns:
            _sr[c] = [int(str(x).replace('%','')) for x in _sr[c]]
            
        p1 = _sr.transpose()[feats].iloc[0].values.tolist()
        p2 = _sr.transpose()[feats].iloc[1].values.tolist()
        p1 = [*p1, p1[0]]
        p2 = [*p2, p2[0]]
        feats = [*feats, feats[0]]

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(p1))

        plt.figure(figsize=(8, 5))
        plt.subplot(polar=True)
        plt.plot(label_loc, p1, label=self.p1_lname)
        plt.plot(label_loc, p2, label=self.p2_lname)
        plt.title(f'{self.p1_lname} vs. {self.p2_lname}', size=20)
        lines, labels = plt.thetagrids(np.degrees(label_loc), labels=feats)
        plt.legend()
        plt.show()


    def build_win_loss_frame(self, p):
        print(p)
        wl = WinLoss(last_name = p)
        player_frames = [ wl.get_overall(), wl.get_pressure(), wl.get_environment(), wl.get_other() ]
        df = pd.concat(player_frames, axis=0, ignore_index=True)
        df.columns = ['index'] + [f'{p}_{c}' for c in df.columns if c != 'index']

        split_list = ['_ytd', '_career']
        for s in split_list:
            label = f'{p}{s}'
            new_label_win = f'{p}{s} wins'
            new_label_loss = f'{p}{s} losses'
            df[[new_label_win, new_label_loss]] = df[label].str.split('-', 1, expand=True)
            df.drop(label, axis=1, inplace=True)
        
        for c in df.columns:
            try:
                df[c] = pd.to_numeric(df[c] )
            except:
                pass

        df.columns = [c.replace(p+'_', '') for c in df.columns]
        
        # cols = ['index'] + ['ytd pct','ytd wins','ytd losses','career pct','career wins','career losses','titles']
        # df = df[cols]

        df.set_index('index', inplace=True)
        return df


    def build_activity_frame(self):
        frames = []
        for p in [self.p1_lname, self.p2_lname]:
            act = Activity(last_name = p, year=self.year)
            df_act = act.get()
            n = len(df_act)
            tourny_frames = []
            for i in range(0, n, 3):
                df = df_act[i+2]
                df['tournament'] = df_act[i][1].iloc[0]
                tourny_frames.append(df)
            
            df = pd.concat(tourny_frames, axis=0, ignore_index=True)
            df['sets'] = df.Score.apply(lambda x: len(str(x).split(' '))) 

            # estimate match date

            df['startdate'] = df['tournament'].apply(lambda x: x.split(' - ')[0].split(' ')[-1])
            df['enddate'] = df['tournament'].apply(lambda x: x.split(' - ')[-1])

            tournaments = df['tournament'].unique()
            df['match_offset'] = ['' for x in range(len(df))]
            myframes = []
            for tournament in tournaments:
                subset = df[df.tournament == tournament]
                min = np.min(subset.index.values)
                max = np.max(subset.index.values)
                for i in range(0, len(subset)):
                    subset['match_offset'].iloc[i] = len(subset)-1-i
                myframes.append(subset)
            
            res = pd.concat(myframes, axis=0)    
            res['startdate'] = pd.to_datetime(res['startdate'])
            res['enddate'] = pd.to_datetime(res['enddate'])
            res['matchdate'] = ['' for x in range(len(res))]
            for i in range(len(res)):
                res['matchdate'].iloc[i] = pd.to_datetime(res['startdate'].iloc[i])+ timedelta(days=res['match_offset'].iloc[i])
                        

            frames.append(res)
        
        return frames[0], frames[1]


    def highlight_wins(self, s):
        return ['background-color: green' if v == 'W' \
                else 'background-color: red' if v == 'L' \
                else '' for v in s]


    def calendar_map(self, data):
        import calmap

        plt.rcParams["figure.figsize"] = (20,3)

        date_index = pd.date_range('1/1/2022', periods=365, freq='D').to_frame()

        data['matchdate'] = pd.to_datetime(data['matchdate'])
        data.set_index('matchdate', inplace = True)

        df = date_index.merge(data, how = 'left', left_index = True, right_index = True)
        df.loc[~df.Opponent.isna(), 'Count'] = 1
        df.fillna(0, inplace = True)
        df.drop([0, 'Opponent'], axis=1, inplace = True)

        calmap.yearplot(df['Count'], year=2022)

        plt.show()

        # https://pythonhosted.org/calmap/
        # calmap.calendarplot(events, monthticks=3, daylabels='MTWTFSS',
        #             dayticks=[0, 2, 4, 6], cmap='YlGn',
        #             fillcolor='grey', linewidth=0,
        #             fig_kws=dict(figsize=(8, 4)))


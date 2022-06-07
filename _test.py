import sys,os
import pandas as pd


from vendors.atp.player import Player
from vendors.atp.stats import Stats
from vendors.atp.winloss import WinLoss
from vendors.atp.activity import Activity

from extract.website import Website

from vendors.tennisabstract.historical_match_stats import HistoricalMatchStats
from vendors.tennisabstract.tennisabstract import TennisAbstract


from vendors.ultimate.ultimatetennis import UltimateTennis

from models import probabilities
from models import learnloop
from models.probabilities import Probabilities

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 12)

'''  vendor data extraction '''
## player stats
# stats = Stats(last_name = 'nadal',  year='2022', surface='clay')
# stats_url = stats.get_player_url()
# print(stats_url)    
# df_serve = stats.get_stats_serve()
# print(df_serve)
# df_return = stats.get_stats_return()
# print(df_return)

## win loss player 
# wl = WinLoss(last_name = 'nadal')
# wl_url = wl.get_player_url()
# print(wl_url)    
# df = wl.get_overall()
# print(df)
# df = wl.get_pressure()
# print(df)
# df = wl.get_environment()
# print(df)
# df = wl.get_other()
# print(df)

# activity player
# act = Activity(last_name = 'nadal', year='2022')
# df_act = act.get()
# n = len(df_act)
# frames = []
# for i in range(0, n, 3):
#     df = df_act[i+2]
#     df['tournament'] = df_act[i][1].iloc[0]
#     frames.append(df)
# df = pd.concat(frames, axis=0, ignore_index=True)
# print(df)

# print(df_act[-1])

#------------------------------------------------------


# ult = UltimateTennis()
# print(ult.get_tournaments())



# tenab = TennisAbstract()
# print(tenab.get_current_event_matches())




#------------------------------------------------------

# hms = HistoricalMatchStats(fname = 'atp_matches_2021.csv')
# df = hms.player_match_rows()
# learnloop.learn(df)



''' game set match and proposition probabilities'''
prob = Probabilities()
ra = prob.expected_rank(atp_rank=1)
rb = prob.expected_rank(atp_rank=100)
print(ra, rb)
pa_match = prob.prob_win_at_match_start(Ra=ra, Rb=rb) # probability of a to win match
print(pa_match)
pa_game  = prob.prob_win_game(Pa=pa_match) # probability of a to win a game
print(pa_game)

point_probs = prob.win_point(ai=0.5, bi=0.5, ci=0.5, aav=0.5, di=0.5, ei=0.5)
print(point_probs)


''' historical match data analysis'''

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

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 12)

'''  vendor data extraction '''
# stats = Stats(last_name = 'djokovic',  year='2021', surface='all')
# stats_url = stats.get_player_url()
# print(stats_url)    

# df_serve = stats.get_stats_serve()
# print(df_serve)

# df_return = stats.get_stats_return()
# print(df_return)

# wl = WinLoss(last_name = 'djokovic')
# wl_url = wl.get_player_url()
# print(wl_url)    
# df_wl = wl.get()
# print(df_wl)

# act = Activity(last_name = 'djokovic')
# act_url = act.get_player_url()
# print(act_url)
# df_act = act.get()
# print(len(df_act))
# print(df_act[0])
# print(df_act[-1])


# ult = UltimateTennis()
# print(ult.get())


# tenab = TennisAbstract().get()
# # tenab.get_current_events_table()
# tenab.get_current_event()

tenab = TennisAbstract()
tenab.get_current_event_matches()


# hms = HistoricalMatchStats(fname = 'atp_matches_2021.csv')
''' historical match data analysis w machine learning'''
# df = hms.player_match_rows()
# print(df.head())
# learnloop.learn(df)


''' game set match and proposition probabilities'''
# probabilities.prob_of_prop_occurance()








''' historical match data analysis'''

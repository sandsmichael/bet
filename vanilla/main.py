import sys,os
from providers.atp.player import Player
from providers.atp.stats import Stats
from extract.website import Website

stats = Stats(last_name = 'djokovic', year='2021', surface='all')

stats_url = stats.get_player_url()
print(stats_url)

df_serve = stats.get_stats_serve()
print(df_serve)

df_return = stats.get_stats_return()
print(df_return)
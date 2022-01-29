import sys,os
from providers.atp.player import Player
from providers.atp.stats import Stats



stats = Stats(last_name = 'djokovic', year='2021', surface='all')
stats_url = stats.get_player_url()
print(stats_url)

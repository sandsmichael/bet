import sys,os
from providers.atp.player import Player
from providers.atp.stats import Stats
from extract.website import Website

stats = Stats(last_name = 'djokovic', year='2021', surface='all')
stats_url = stats.get_player_url()
print(stats_url)

web = Website(url = stats_url)
web.scrape()
frames  = web.scrape_table_to_df(div_node='id', div_identifier='playerMatchFactsContainer')
df_serve, df_return = frames[0], frames[1]
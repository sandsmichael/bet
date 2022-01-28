import sys,os
from providers.atp import Atp 

atp = Atp()
player_links = atp.get_top_players_links(n=100)

id_dict = atp.extract_player_id_from_url(urls = player_links)
print(id_dict)
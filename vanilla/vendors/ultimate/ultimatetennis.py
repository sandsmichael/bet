


import sys,os
import pandas as pd
from extract.website import Website
from vendors.provider import Provider

class UltimateTennis(Provider):

    def __init__(self):
        super().__init__()
        self.name = "UltimateTennis"
        self.base_url = "https://www.ultimatetennisstatistics.com"
        self.live_scores = self.base_url + "/liveScores"
        self.tournaments = self.base_url + "/tournamentEvents"


    def get_tournaments(self):
        web = Website(url = self.live_scores)
        web.scrape_headless()
        print(web.soup)
        # childs = web.get_all_children_of_elem(elm='tr', attrib='data-row-id', attrib_value='1', child_node='td')
        # print(childs)        
        # web.parse_html(elm='a', attrib='title', value='Enetscores by Enetpulse' )





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


    def get(self):
        web = Website(url = self.live_scores)
        web.scrape()
        print(web.soup)
        return web.parse_html(elm='div', attrib='class', value='wff_tennis_event_row', )



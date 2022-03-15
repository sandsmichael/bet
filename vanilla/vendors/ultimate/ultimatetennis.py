


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
        web = Website(url = self.base_url)
        web.scrape()

        df =  web.parse_html(elm = 'div', attrib='class', value='wff_tennis_event' )
        print(df)

        # web.parse_html(elm='a', attrib='title', value='Enetscores by Enetpulse' )





import sys,os
import pandas as pd
from extract.website import Website
from vendors.provider import Provider

class UltimateTennis(Provider):

    def __init__(self):
        super().__init__()
        self.name = "UltimateTennis"
        self.atp_url = "https://www.ultimatetennisstatistics.com/"


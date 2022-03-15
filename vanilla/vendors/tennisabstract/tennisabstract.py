import sys,os
import pandas as pd
from extract.website import Website
from vendors.provider import Provider

class TennisAbstract(Provider):

    def __init__(self):
        super().__init__()
        self.name = "TennisAbstract"
        self.base_url = "https://www.tennisabstract.com/"

    def get(self):
        web = Website(url = self.base_url)
        web.scrape()
        links =  web.get_links()
        print(links)


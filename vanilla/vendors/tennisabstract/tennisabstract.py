import sys,os
import pandas as pd
from extract.website import Website
from vendors.provider import Provider

class TennisAbstract(Provider):

    def __init__(self):
        super().__init__()
        self.name = "TennisAbstract"
        self.base_url = "https://www.tennisabstract.com/"

        # self.get()


    def get(self):
        self.web = Website(url = self.base_url)
        self.web.scrape()


    def get_current_events_table(self):
        df =  self.web.scrape_table_to_df(elm = 'table', attrb='id', value='current-events' )
        print(df)


    def get_current_event_url(self):
        links = self.web.get_links()
        res = [l for l in links if '/current/' and 'ATP' in l and '_' not in l]

        if isinstance(res, list):
            self.current_event_url  = res[0]
        else:
            self.current_event_url  = res
        return self.current_event_url
        

    def get_current_events(self):
        event_url = self.get_current_event_url()
        print(event_url)
        web = Website(url = event_url)
        # web.scrape()
        # print(web.scrape)
        # df = web.get_all_children_of_div(elm='span', attrib='id', attrib_value='upcoming', child_node='a')
        df = web.get_links()
        print(df)
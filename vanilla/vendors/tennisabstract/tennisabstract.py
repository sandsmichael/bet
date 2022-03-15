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


    def get_current_event(self):
        links = self.web.get_links()
        res = [l for l in links if '/current/' and 'ATP' in l and '_' not in l]

        if isinstance(res, list):
            self.current_event_url  = res[0]
        else:
            self.current_event_url  = res
        return self.current_event_url
        


class TennisAbstractEvent(TennisAbstract):
    """ example  event:
    http://www.tennisabstract.com/current/2022ATPIndianWells.html

    """

    def __init__(self):
        super().__init__()
        super().get()
        self.event = self.get_current_event()
        print(self.event)
        self.get()


    def get(self):
        self.web = Website(url = self.event)
        self.web.scrape()


    def upcoming_matches(self):
        res  = self.web.get_all_children_of_div(elm='span', attrib='id', attrib_value='upcoming', child_node = 'a')
        print(res)

        table = self.web.soup.find_all('table')
        frames = pd.read_html(str(table))
        print(len(frames))
        print(frames[2].iloc[0].values)

        return res


    def completed():
        pass

    def forecasts():
        pass

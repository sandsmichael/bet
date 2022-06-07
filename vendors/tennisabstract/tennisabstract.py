from random import weibullvariate
import sys,os
import pandas as pd
from extract.website import Website,  WebBot
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
        """ return the url for the current atp event"""
        links = self.web.get_links()
        res = [l for l in links if '/current/' and 'ATP' in l and '_' not in l]

        if isinstance(res, list):
            self.current_event_url  = res[0] #FIXME; get all events
        else:
            self.current_event_url  = res
        return self.current_event_url
        

    def get_current_event_matches(self):
        """[Summary]
        :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: a list of current matches with both players stored as a tuple with the format (player1, player2)
        :rtype: list(tuples)
        """        
        self.get()
        event_url = self.get_current_event_url()
        web = Website(event_url)
        web.scrape_headless()
        childs = web.get_all_children_of_elem(elm='span', attrib='id', attrib_value='upcoming', child_node='a')
        childs  = [str(c.get_text()) for c in childs if ('[' and ']')  not in str(c)] # values displaying H2H record are displayed like '[#-#]'
        
        assert(len(childs)%2 == 0,) # even number of players in events url's being retreived

        matches = [*zip(childs[::2], childs[1::2])] # slice in pairs of two and zip!
        return matches

        


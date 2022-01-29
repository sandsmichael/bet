from bs4 import BeautifulSoup
import requests
import pandas as pd

class Website:

    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    def __init__(self, url:str):
        self.url = url

    def scrape(self):
        req = requests.get(self.url, self.headers)
        self.soup = BeautifulSoup(req.content, 'html.parser')
        return self.soup

    def get_links(self):
        soup = self.scrape()
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return urls

    def get_all_children_of_div(self, div_node:str, div_identifier:str=None, child_node:str=None):
        """[]

        :param [div_node]: ["id" or "class"], defaults to [None]
        :param [div_identifier]: [identifier string of the div_node], defaults to [None]
        :param [child_node]: [identifier of the chid node object type to find], defaults to [None]
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [links]
        :rtype: [list]
        """
        divTag = self.soup.find_all("div", {div_node: div_identifier})
        print(divTag)
        for tag in divTag:
            tdTags = tag.find_all(child_node)
            for tag in tdTags:
                print(tag.text)

    def scrape_table_to_df(self, div_node:str, div_identifier:str=None,  ):
        """[]

        :param [div_node]: ["id" or "class"], defaults to [None]
        :param [div_identifier]: [identifier string of the div_node], defaults to [None]
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [list of dataframes]
        :rtype: [list]
        """
        table = self.soup.find_all("div", {div_node: div_identifier})
        frames = pd.read_html(str(table))
        return frames

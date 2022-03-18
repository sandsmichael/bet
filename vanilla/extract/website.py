from bs4 import BeautifulSoup
import requests
import pandas as pd

class Website:

    headers_x = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    headers_y = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", 
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

    def __init__(self, url:str):
        self.url = url


    def scrape(self, req_session:bool=True, headers=headers_x):
        """[Summary]

        :param req_session: bool to  scrapee with requests.seession or requests.get
            sends default headeer of >>> session.headers['User-Agent'] > 'python-requests/2.19.1'
            https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending
        """
        self.headers= headers

        if req_session==False:
            response = requests.get(self.url, self.headers)
        else:
            response = requests.Session().get(self.url, headers=self.headers)

        self.soup = BeautifulSoup(response.content, 'html.parser')
        return self.soup


    def get_links(self):
        soup = self.scrape()
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return urls

    def get_all_children_of_div(self, elm:str, attrib:str, attrib_value:str=None, child_node:str=None):
        """[]
            elm =  div, span. etc
        :param [attrib]: ["id" or "class"], defaults to [None]
        :param [attrib_value]: [identifier string of the div_node], defaults to [None]
        :param [child_node]: [identifier of the chid node object type to find], defaults to [None]

        :raises [ErrorType]: [ErrorDescription]

        :return: [links]
        :rtype: [list]
        """
        from bs4 import BeautifulSoup, NavigableString, Tag

        myTag = self.soup.find(elm, {attrib: attrib_value}) 
        for tag in myTag:
            for body_child in myTag.children:
                if isinstance(body_child, NavigableString):
                    continue
                if isinstance(body_child, Tag):
                    tdTags = tag.findChildren(child_node, recursive=True)
                    for tag in tdTags:
                        print(tag)

        # return myTag


    def scrape_table_to_df(self, elm = 'div', attrb:str='id', value:str=None,  ):
        """[]

        :param [div_node]: ["id" or "class"], defaults to [None]
        :param [div_identifier]: [identifier string of the div_node], defaults to [None]

        :raises [ErrorType]: [ErrorDescription]

        :return: [list of dataframes]
        :rtype: [list]
        """
        table = self.soup.find_all(elm, {attrb: value})
        frames = pd.read_html(str(table))
        return frames


    def parse_html(self, elm='div', attrib='class', value=None):
        return self.soup.find_all(elm, {attrib: value})

from bs4 import BeautifulSoup
import requests


class Website:

    def __init__(self, url:str):
        self.url = url

    
    def get_links(self):
        reqs = requests.get(self.url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return urls
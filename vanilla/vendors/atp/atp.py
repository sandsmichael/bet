import sys,os
import pandas as pd
from extract.website import Website
from vendors.provider import Provider

class Atp(Provider):

    def __init__(self):
        super().__init__()
        self.name = "ATP"
        self.atp_url = "https://www.atptour.com/"


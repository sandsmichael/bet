class Provider:
    
    def __init__(self, name:str=None, url:str=None):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name

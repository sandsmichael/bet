import sys,os

from provider import Provider

class Atp(Provider):

    def __init__(self):
        super.__init__()
        self.name = "ATP"
        self.url = "https://www.atptour.com/en/"





    def get_player_id():
        pass

    def get_top_player_ids(self, n:int=100):
        """[retreive atp.com player ids for top n players]

        :param [n]: [number of players], defaults to [100]
        :type [ParamName]: [ParamType](, optional)
        ...
        :raises [ErrorType]: [ErrorDescription]
        ...
        :return: [ReturnDescription]
        :rtype: [ReturnType]
        """
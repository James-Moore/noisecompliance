from urllib3.util.url import Url
from situationalawareness.perceptionstage.abstractclient import AbstractClient

class NoiseClient(AbstractClient):
    def __init__(self, clientURL: Url):
        self.decibleURL = clientURL.url+'/getDecible'
        self.shutdownURL = clientURL.url+'/shutdown'
        super().__init__(clientURL)

    def getDecibleURL(self):
        return self.decibleURL

    def setDecibleURL(self, url):
        self.decibleURL = url

    def getDecible(self):
        return self.restfulGet(self.getDecibleURL())
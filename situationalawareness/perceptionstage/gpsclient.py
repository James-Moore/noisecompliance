from urllib3.util.url import Url
from situationalawareness.perceptionstage.abstractclient import AbstractClient

class GpsClient(AbstractClient):
    def __init__(self, clientURL: Url):
        self.longitudeURL = clientURL.url + '/getLongitude'
        self.latitudeURL = clientURL.url + '/getLatitude'
        super().__init__(clientURL)

    def getLongitudeURL(self):
        return self.longitudeURL

    def setLongitudeURL(self, locator: Url):
        self.longitudeURL = locator.url

    def getLatitudeURL(self):
        return self.latitudeURL

    def setLatitudeURL(self, locator: Url):
        self.latitudeURL = locator.url

    def getLongitude(self):
        return self.restfulGet(self.getLongitudeURL())

    def getLatitude(self):
        return self.restfulGet(self.getLatitudeURL())
import requests
from urllib3.util import Url

from gps.abstractgps import AbstractGPS


class IpGPS(AbstractGPS):
    def __init__(self):
        self.SCHEME="http"
        self.HOSTNAME="ipinfo.io"
        self.PATH="/loc"
        self.COORDINATES_URL = Url(scheme=self.SCHEME, host=self.HOSTNAME, path=self.PATH)
        super().__init__()
        self.update()

    def getConstants(self):
        return self.constants

    def update(self):
        print(self.COORDINATES_URL.url)
        r = requests.get(self.COORDINATES_URL.url)
        coordinates: list = eval(r.text)
        self.setLatitude(coordinates[0])
        self.setLongitude(coordinates[1])
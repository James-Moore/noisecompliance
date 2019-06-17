from situationalawareness.perceptionstage.gpsclient import GpsClient
from situationalawareness.perceptionstage.noiseclient import NoiseClient
from situationalawareness.perceptionstage.environment import Environment
from urllib3.util.url import Url
import pprint
import time

class Perception:
    def __init__(self, noiseClientURL: Url, gpsClientUrl: Url):
        self.noiseClient = NoiseClient(noiseClientURL)
        self.gpsClient = GpsClient(gpsClientUrl)
        self.environment = Environment()
        self.perceiveEnvironment()

    def perceiveEnvironment(self):
        self.updateNoiseLevel()
        self.updateGPS()

    def updateNoiseLevel(self):
        try:
            noiseLevel = self.getNoiseClient().getDecible()
            self.getEnvironment().setNoiseLevel(noiseLevel)
        except Exception:
            self.getEnvironment().setNoiseLevel(float('-inf'))
            pass

    def updateGPS(self):
        longitude = float('-inf')
        latitude = float('-inf')
        try:
            longitude = self.getGpsClient().getLongitude()
            latitude = self.getGpsClient().getLatitude()
        except Exception:
            pass
        finally:
            self.getEnvironment().setLongitude(longitude)
            self.getEnvironment().setLatitude(latitude)


    def getEnvironment(self):
        return self.environment

    def getNoiseClient(self):
        return self.noiseClient

    def getGpsClient(self):
        return self.gpsClient

    def isValid(self):
        return self.getEnvironment().isValid()
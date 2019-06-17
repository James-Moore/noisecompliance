import json
from abc import ABC
from abc import abstractmethod

from gps.gpsconstants import GPSConstants


class AbstractGPS(ABC):
    def __init__(self):
        self.longitude = 0.0
        self.latitude = 0.0
        super().__init__()

    def __str__(self):
        return str(self.toArray())

    def getLongitude(self):
        return self.longitude

    def setLongitude(self, longitude):
        self.longitude = longitude

    def getLatitude(self):
        return self.latitude

    def setLatitude(self, latitude):
        self.latitude = latitude

    def longitudeAsJSON(self):
        dict = {
            GPSConstants.LONGITUDE: self.getLongitude()
        }
        return json.dumps(dict)

    def latitudeAsJSON(self):
        dict = {
            GPSConstants.LATITUDE: self.getLatitude()
        }
        return json.dumps(dict)

    def toJSON(self):
        dict = {
            GPSConstants.LONGITUDE: self.getLongitude(),
            GPSConstants.LATITUDE: self.getLatitude()
        }
        return json.dumps(dict)


    def toArray(self):
        return [self.getLongitude(), self.getLatitude()]

    @abstractmethod
    def update(self):
        pass

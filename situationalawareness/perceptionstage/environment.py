from situationalawareness.comprehensionstage import TCONST

class Environment:
    def __init__(self):
        self.noiseLevel = float('-inf')
        self.longitude = float('-inf')
        self.latitude = float('-inf')

    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        out = {
            'NoiseLevel': self.getNoiseLevel(),
            'Longitude': self.getLongitude(),
            'Latitude': self.getLatitude()
        }

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def getNoiseLevel(self):
        return self.noiseLevel

    def setNoiseLevel(self, noiseLevel):
        self.noiseLevel = noiseLevel

    def getLongitude(self):
        return self.longitude

    def setLongitude(self, longitude):
        self.longitude = longitude

    def getLatitude(self):
        return self.latitude

    def setLatitude(self, latitude):
        self.latitude = latitude

    def getCoordinates(self):
        coord = [self.getLongitude(), self.getLatitude()]
        return coord

    def deepCopy(self):
        e = Environment()
        e.setNoiseLevel(self.getNoiseLevel())
        e.setLongitude(self.getLongitude())
        e.setLatitude(self.getLatitude())
        return e

    def isValid(self):
        latValid = self.getLatitude() != float('-inf')
        longValid = self.getLatitude() != float('-inf')
        noiseValid = self.getNoiseLevel() != float('-inf')
        return  latValid and longValid and noiseValid
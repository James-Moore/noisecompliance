import time
import uuid
from situationalawareness.comprehensionstage.movingaverage import MovingAverage
from situationalawareness.compliance.windowpolicy import WindowPolicy
from situationalawareness.comprehensionstage.abstracttracker import AbstractTracker
from situationalawareness.perceptionstage.environment import Environment
from situationalawareness.comprehensionstage import TCONST
import json
import copy

class WindowTracker(AbstractTracker):
    def __init__(self, windowPolicy: WindowPolicy, environment: Environment):
        super().__init__(windowPolicy, environment)
        self.startTime = time.time()
        self.endTime = self.getStartTime() + self.getWindowSize()
        self.movingAverage = MovingAverage()

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def __str__(self):
        out = str(self.toDict())
        return out

    def toDict(self):
        out = super().toDict()
        out.update({TCONST.NOISE_AVG: str(self.getAverageNoiseLevel())})
        out.update({TCONST.WIN_SIZE: str(self.getWindowSize())})
        out.update({TCONST.TIME_START: self.getFormatedStartTime()})
        out.update({TCONST.TIME_END: self.getFormatedEndTime()})
        out.update({TCONST.TIME_CUR: time.asctime(time.localtime(time.time()))})
        return out

    def getWindowSize(self):
        return self.getPolicy().getWindowSize()

    def getFormatedStartTime(self):
        return time.asctime(time.localtime(self.getStartTime()))

    def getFormatedEndTime(self):
        return time.asctime(time.localtime(self.getEndTime()))

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime

    def getRemainingWindow(self):
        currentTime = time.time()
        remainingTime = self.getEndTime()-currentTime
        return remainingTime

    def getMovingAverage(self):
        return self.movingAverage

    def getAverageNoiseLevel(self):
        return self.getMovingAverage().getAverage()

    def setMovingAverage(self, movingAverage):
        self.movingAverage = movingAverage

    def setStartTime(self, t):
        self.startTime = t

    def setEndTime(self, t):
        self.endTime = t

    def update(self, enviroment: Environment ):
        self.getMovingAverage().update(enviroment.getNoiseLevel())
        super().update(enviroment)

    def createResetReplicaTracker(self):
        replicaTracker = WindowTracker(self.getPolicy(), self.getEnvironment())
        '''
        print("WIN_TRKR-ORIG: "+str(self))
        print("WIN_TRKR-RPLCA: " + str(replicaTracker))
        '''
        return replicaTracker

    def hasBrokenPolicy(self):
        return (self.getAverageNoiseLevel() > self.getPolicy().getThreshold())

    def isExpired(self):
        return (self.getEndTime() <= time.time())

    def isConcrete(self):
        return True

    def trackerType(self):
        return TCONST.TYPE_WIN

    def deepCopy(self):
        env = copy.deepcopy(self.getEnvironment())
        pol = copy.deepcopy(self.getPolicy())
        avg = self.getMovingAverage().deepCopy()
        out = WindowTracker(pol, env)
        out.setMovingAverage(avg)
        out.setStartTime(self.getStartTime())
        out.setEndTime(self.getEndTime())
        return out
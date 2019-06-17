from situationalawareness.compliance.impulsepolicy import ImpulsePolicy
from situationalawareness.comprehensionstage.abstracttracker import AbstractTracker
from situationalawareness.perceptionstage.environment import Environment
from situationalawareness.comprehensionstage import TCONST
import copy
import time

class ImpulseTracker(AbstractTracker):
    def __init__(self, impulsePolicy : ImpulsePolicy, environment: Environment):
        self.impulse = environment.getNoiseLevel()
        self.impulseTime = time.asctime(time.localtime(time.time()))
        super().__init__(impulsePolicy, environment)

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def __str__(self):
        out = str(self.toDict())
        return out

    def toDict(self):
        out = super().toDict()
        out.update({TCONST.NOISE_IMP: str(self.getImpulseLevel())})
        out.update({TCONST.TIME_IMP: self.getImpulseLevelTime()})
        out.update({TCONST.TIME_CUR: time.asctime(time.localtime(time.time()))})
        return out

    def getImpulseLevel(self):
        return self.impulse

    def setImpulseLevel(self, level):
        self.impulse = level

    def getImpulseLevelTime(self):
        return self.impulseTime

    def setImpulseLevelTime(self, t):
        self.impulseTime = t

    def updateImpulseLevelTime(self):
        self.setImpulseLevelTime(time.asctime(time.localtime(time.time())))

    def reset(self):
        self.impulse = self.getEnvironment().getNoiseLevel()
        self.updateImpulseLevelTime()

    def update(self, environment: Environment):
        old = self.getImpulseLevel()
        new = max(old, environment.getNoiseLevel())

        if old != new:
            self.setImpulseLevel(new)
            self.updateImpulseLevelTime()

        super().update(environment)

    def deepCopy(self):
        env = copy.deepcopy(self.getEnvironment())
        pol = copy.deepcopy(self.getPolicy())
        out = ImpulseTracker(pol, env)
        out.setImpulseLevel(self.getImpulseLevel())
        out.setImpulseLevelTime(self.getImpulseLevelTime())
        return out

    def hasBrokenPolicy(self):
        return (self.getImpulseLevel() > self.getThreshold())

    def isConcrete(self):
        return True

    def trackerType(self):
        return TCONST.TYPE_IMP
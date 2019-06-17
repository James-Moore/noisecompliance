import copy
import json
import uuid
from collections import defaultdict
from datetime import datetime, timedelta

from situationalawareness.comprehensionstage.situation import Situation


class Projection:
    def __init__(self):
        self.policyVolations = defaultdict(list)
        self.impulseViolated = False
        self.impulseTimer = 10 #clear impulse violation after this many seconds
        self.impulseClearTime = datetime.now().time()

    def getPolicyViolationsLen(self):
        size = 0
        for key in self.getPolicyViolations().keys():
            vals = len(self.getPolicyViolations()[key])
            size = size + vals
        return size

    def getPolicyViolationsAsJSON(self):
        out = list()
        for key in self.getPolicyViolations().keys():
            for val in self.getPolicyViolations()[key]:
                out.append(val.toDict())

        return json.dumps(out)

    #if you do a direct index on the returned defaultdict (Ex: getpolicyVilations()[SOMEVAL]) defaultdict will create
    #an empty element with the key indexed in defaultdict, which is totally counter intuitive.  BEWARE
    def getPolicyViolations(self):
        return self.policyVolations

    def addPolicyViolation(self, tracker):
        trackerCopy = copy.deepcopy(tracker)
        self.getPolicyViolations()[trackerCopy.getID()].append(trackerCopy)

    def removePolicyViolations(self, id: uuid):
        try:
            self.getPolicyViolations().pop(id)
        except Exception as e:
            pass

    def getImpulseTimer(self):
        return self.impulseTimer

    def getImpulseClearTime(self):
        return self.impulseClearTime

    def setImpulseClearTime(self, clearTime):
        self.impulseClearTime = clearTime

    def updateImpulseClearTime(self):
        now = datetime.now()
        delta = timedelta(seconds=self.getImpulseTimer())
        clearTime = now + delta
        self.setImpulseClearTime(clearTime.time())

    def hasImpulseViolated(self):
        return self.impulseViolated

    def setImpulseViolated(self, violated: bool):
        self.impulseViolated = violated

    def impulseCanClear(self):
        return (self.getImpulseClearTime() < datetime.now().time())

    def projectImpulse(self, situation: Situation):
        impulseTracker = situation.getImpulseTracker()
        if impulseTracker.hasBrokenPolicy():
            self.addPolicyViolation(impulseTracker.deepCopy())
            self.setImpulseViolated(True)
            self.updateImpulseClearTime()
            impulseTracker.reset()

    def projectWindow(self, situation):
        expiredTrackers: set = situation.getExpiredTrackers()

        for tracker in expiredTrackers:
            if tracker.hasBrokenPolicy():
                self.addPolicyViolation(tracker)

        expiredTrackers.clear()


    def project(self, situation: Situation):
        if not self.hasImpulseViolated():
            self.projectImpulse(situation)
        else:
            if self.impulseCanClear():
                self.setImpulseViolated(False)
                situation.getImpulseTracker().reset()

        self.projectWindow(situation)

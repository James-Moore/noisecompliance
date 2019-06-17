from situationalawareness.perceptionstage.perception import Perception
from situationalawareness.comprehensionstage.comprehension import Comprehension
from situationalawareness.projectionstage.projection import Projection
from situationalawareness.compliance.policies import Policies
from situationalawareness.compliance.impulsepolicy import ImpulsePolicy
from situationalawareness.compliance.windowpolicy import WindowPolicy
from situationalawareness.comprehensionstage.situation import Situation
from threading import Thread, Event, Lock
from common.configurls import URLConfigs
import uuid
import copy
import pprint
import time
from common.configurls import URLConfigs

class SituationalAwareness(Thread):
    def __init__(self, stopEvent : Event, lock : Lock, policies: Policies, urls: URLConfigs):
        self.stopEvent = stopEvent
        self.lock = lock
        self.policies = policies
        self.perception = Perception(urls.MIC_HOST, urls.GPS_HOST)
        self.perception.perceiveEnvironment()
        self.comprehension = Comprehension(self.policies, self.perception.getEnvironment())
        self.projection = Projection()
        Thread.__init__(self)

    def removeWindowPolicy(self, id: uuid):
        stage1 = True
        stage2 = True

        try:
            self.getProjection().removePolicyViolations(id)
        except:
            stage1 = False

        try:
            stage2 = self.getPolicies().removeWindowPolicy(id)
        except:
            stage2 = False

        return (stage1 and stage2)



    def getBrokenPolicies(self):
        out = list()
        removeNones = set()

        for key in self.getProjection().getPolicyViolations().keys():
            p = self.getPolicies().getPolicy(key)
            if(p is not None):
                out.append(p.toDict())
            else:
                removeNones.add(key)

        for key in removeNones:
            self.getProjection().removePolicyViolations(key)

        return out

#TODO SOMETHING STRANGE IS HAPPENING WITH getPolicyViolations()[id] where if the id does not exist it is added as a value and the id is added as a key
    def getBrokenPolicy(self, id: uuid):
        out = list()
        for tracker in self.getProjection().getPolicyViolations()[id]:
            out.append(tracker.toDict())

        return out

    def getPolicies(self):
        return self.policies

    def getLock(self):
        return self.lock

    def isStopSet(self):
        return self.stopEvent.is_set()

    def getProjection(self):
        return self.projection

    def getPerception(self):
        return self.perception

    def getComprehension(self):
        return self.comprehension

    def percieve(self):
        self.getPerception().perceiveEnvironment()

    def comprehend(self):
        environment = self.getPerception().getEnvironment()
        self.getLock().acquire()
        try:
            self.getComprehension().comprehendSituation(self.getPolicies(), environment)
        finally:
            self.getLock().release()

    def project(self):
        situation: Situation = None
        self.getLock().acquire()
        try:
            situation = self.getComprehension().getSituation()
        finally:
            self.getLock().release()

        self.projection.project(situation)

    def becomeAware(self):
        while not self.isStopSet():
            self.percieve()
            if self.getPerception().isValid():
                self.comprehend()
                self.project()
                time.sleep(.01)
            else:
                print("****Waiting for dependent services to start...  Will sleep a couple seconds****", end="", flush=True)
                time.sleep(2)
                print("\r", end="", flush=True)
                time.sleep(2)


    def run(self):
        self.becomeAware()
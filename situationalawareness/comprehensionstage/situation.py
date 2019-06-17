from situationalawareness.comprehensionstage.impulsetracker import ImpulseTracker
from situationalawareness.comprehensionstage.windowtracker import WindowTracker
from situationalawareness.compliance.policies import Policies
from situationalawareness.perceptionstage.environment import Environment
import pprint
import uuid
import json


class Situation:

    def __init__(self, policies: Policies, environment: Environment):
        self.impulseTracker = ImpulseTracker(policies.getImpulsePolicy(), environment)
        self.windowTrackers = set()
        self.expiredWindowTrackers = set()

        for windowPolicy in policies.getWindowPoliciesDict().values():
            self.windowTrackers.add(WindowTracker(windowPolicy, environment))

    def __str__(self):
        self.toString()

    def toString(self):
        out = "\rCurrent Level: " + str(self.getImpulseTracker().getCurrentNoise()) + \
              "\tImpulse: " + str(self.getImpulseTracker().getImpulseLevel()) + \
              "\tWindows-Active: " + str(len(self.getWindowTrackers())) + \
              "\tWindows-Expired: " + str(len(self.getExpiredTrackers()))
        return out

    def printSummary(self):
        print(self.toString(), end='')

    def getImpulseTracker(self):
        return self.impulseTracker

    def getWindowTrackers(self):
        return self.windowTrackers

    def getExpiredTrackers(self):
        return self.expiredWindowTrackers

    def getTrackerJSON(self, policyID : uuid):
        pass

    #policyID is uuid4
    def containsTracker(self, policyID: uuid):
        out = False

        if(self.getImpulseTracker().isTracker(policyID)):
            out = True

        for tracker in self.getWindowTrackers():
            if tracker.isTracker(policyID):
                out = True
                break

        return out

    #pre: verification performed ensuring policy exists
    def getTracker(self, policyID: uuid):

        if (self.getImpulseTracker().isTracker(policyID)):
            return self.getImpulseTracker()

        for tracker in self.getWindowTrackers():
            if tracker.isTracker(policyID):
                return tracker

        return None

    # private, used by update
    def handleExpiredTrackers(self):
        replicaTrackers = set()

        for windowTracker in self.getWindowTrackers():
            if (windowTracker.isExpired()):
                self.getExpiredTrackers().add(windowTracker)
                replicaTrackers.add(windowTracker.createResetReplicaTracker())

        self.getWindowTrackers().difference_update(self.getExpiredTrackers())
        self.getWindowTrackers().update(replicaTrackers)

    def removeStaleTrackers(self, policies: Policies):
        removeTrackers = set()
        removeExpTrackers = set()


        for tracker in self.getWindowTrackers():
            if(policies.containsPolicy(tracker.getID()) == False):
                removeTrackers.add(tracker)

        for tracker in self.getExpiredTrackers():
            if (policies.containsPolicy(tracker.getID()) == False):
                removeExpTrackers.add(tracker)

        self.getWindowTrackers().difference_update(removeTrackers)
        self.getExpiredTrackers().difference_update(removeExpTrackers)

    def createNewTrackers(self, policies: Policies, environment: Environment):
        #get all the keys for existing window trackers
        trackerKeys = set()
        for tracker in self.getWindowTrackers():
            trackerKeys.add(tracker.getID())

        #get all the keys for required policies
        policyKeys = policies.getWindowPoliciesDict().keys()

        #find the policies that do not have trackers instantiated
        requiredKeys = policyKeys - trackerKeys

        #instantiate required trackers
        requiredTrackers = set()
        for key in requiredKeys:
            addTracker = WindowTracker(policies.getWindowPolicy(key), environment)
            requiredTrackers.add(addTracker)

        #add required trackers
        self.getWindowTrackers().update(requiredTrackers)

    def updatePolicies(self, policies: Policies, environment):
        self.removeStaleTrackers(policies)
        self.createNewTrackers(policies, environment)



    #private, used by update
    def updateWindowTrackers(self, environment: Environment):
        for windowTracker in self.getWindowTrackers():
            windowTracker.update(environment)

    #private, used by update
    def updateImpulseTracker(self, environment: Environment):
        self.getImpulseTracker().update(environment)

    # private, used by update
    def updateTrackers(self, environment: Environment):
        self.updateImpulseTracker(environment)
        self.updateWindowTrackers(environment)

    #use to update current comprehension of the situation
    def update(self, policies: Policies, environment: Environment):
        self.updatePolicies(policies, environment)
        self.handleExpiredTrackers()
        self.updateTrackers(environment)
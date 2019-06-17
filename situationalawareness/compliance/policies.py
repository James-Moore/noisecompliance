import uuid
import json
from flask import jsonify
from situationalawareness.compliance.windowpolicy import WindowPolicy
from situationalawareness.compliance.impulsepolicy import ImpulsePolicy
from threading import Lock
'''
        self.lock.acquire()
        try:
        
        finally:
            self.lock.release()

'''

class Policies:

    def __init__(self, impulsePolicy: ImpulsePolicy, windowPolicies: set): # windowPolicies is a dictionary of type dict[uuid, WindowPolicy]
        self.lock = Lock()
        self.impulsePolicy = impulsePolicy
        self.windowPoliciesDict = dict()
        for windowPolicy in windowPolicies:
            self.addWindowPolicy(windowPolicy)

    def toJSON(self):
        out = list()
        self.lock.acquire()
        try:
            out.append(self.getImpulsePolicy().toDict())

            for windowPolicy in self.getWindowPoliciesDict().values():
                out.append(windowPolicy.toDict())
        finally:
            self.lock.release()
            return jsonify({'policies': out})

    def policyAsJSON(self, policyID):
        out = dict()
        self.lock.acquire()
        try:
            out = self.getPolicy(policyID).toDict()
        finally:
            self.lock.release()
            return jsonify({'policy': out})

    def asPrintableList(self):
        out = list()
        self.lock.acquire()
        try:
            out.append(self.getImpulsePolicy().toDict())
            for windowPolicy in self.getWindowPoliciesDict().values():
                out.append(windowPolicy.toDict())
        finally:
            self.lock.release()
            return out

    def getImpulsePolicy(self):
        return self.impulsePolicy

    def getWindowPoliciesDict(self):
        return self.windowPoliciesDict

    #policyID is uuid4
    def containsPolicy(self, policyID: uuid):
        out = False
        self.lock.acquire()
        try:
            if (self.getImpulsePolicy().isPolicy(policyID)):
                out = True
            elif (policyID in self.getWindowPoliciesDict()):
                out = True
        finally:
            self.lock.release()
            return out

    #pre: verification performed ensuring policy exists
    def getPolicy(self, policyID: uuid):
        if (self.getImpulsePolicy().isPolicy(policyID)):
            return self.getImpulsePolicy()
        else:
            return self.getWindowPoliciesDict().get(policyID)

    def removeWindowPolicy(self, policyID: uuid):
        out = False
        self.lock.acquire()
        try:
            if(self.getImpulsePolicy().isPolicy(policyID)):
                out = True
            else:
                self.getWindowPoliciesDict().pop(policyID)
                out = True
        except Exception as e:
            pass
        finally:
            self.lock.release()
            return out

    def getWindowPolicy(self, policyID):
        return self.getWindowPoliciesDict().get(policyID)

    def addWindowPolicy(self, windowPolicy: WindowPolicy):
        self.lock.acquire()
        try:
            self.getWindowPoliciesDict().update({windowPolicy.getPolicyID(): windowPolicy})
        finally:
            self.lock.release()

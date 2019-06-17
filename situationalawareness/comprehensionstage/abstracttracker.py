from abc import ABC
from abc import abstractmethod
from situationalawareness.compliance.policy import Policy
from situationalawareness.perceptionstage.environment import Environment
from situationalawareness.comprehensionstage import TCONST
import uuid
from flask import jsonify
import pprint


class AbstractTracker(ABC):
    def __init__(self, policy: Policy, environment: Environment):
        self.policy = policy
        self.environment = environment
        super().__init__()

    # is this class associated with the given policy
    def associatedWith(self, policy):
        return self.getPolicy().getPolicyID() == policy.getPolicyID()

    def getPolicy(self):
        return self.policy

    def getThreshold(self):
        return self.getPolicy().getThreshold()

    def getEnvironment(self) -> Environment:
        return self.environment

    def getCurrentNoise(self):
        e = self.getEnvironment()
        l = e.noiseLevel
        return l

    def getID(self):
        return self.getPolicy().getPolicyID()

    def isTracker(self, policyID : uuid ):
        return self.getPolicy().isPolicy(policyID)

    def toDict(self):
        out = {
            TCONST.ID: self.getID(),
            TCONST.TYPE: self.trackerType(),
            TCONST.NOISE_CUR: self.getCurrentNoise(),
            TCONST.COORD: self.getEnvironment().getCoordinates(),
            TCONST.NOISE_THRES: str(self.getThreshold())
        }
        return out

    def toJSON(self):
        return jsonify({TCONST.TRACKER: self.toDict()})

    @abstractmethod
    def trackerType(self):
        pass

    @abstractmethod
    def hasBrokenPolicy(self):
        pass

    @abstractmethod
    def isConcrete(self):
        pass

    @abstractmethod
    def update(self, environment: Environment):
        self.environment = environment
        pass

    @abstractmethod
    def deepCopy(self):
        pass
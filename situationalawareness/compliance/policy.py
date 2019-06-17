from abc import ABC, abstractmethod
from situationalawareness.comprehensionstage import TCONST
import uuid
import json

class Policy(ABC):
    def __init__(self, threshold: float):
        self.policyID = uuid.uuid4()
        self.threshold = threshold
        super().__init__()

    def instanceClassName(self):
        return type(self).__name__

    def getThreshold(self):
        return self.threshold

    def getPolicyID(self):
        return self.policyID

    def getPolicyIdAsString(self):
        return str(self.getPolicyID())

    def isPolicy(self, policyID: uuid):
        return (str(policyID) == self.getPolicyIdAsString())

    def toDict(self):
        out = {
            TCONST.ID: self.getPolicyIdAsString(),
            TCONST.TYPE: self.policyType(),
            TCONST.NOISE_THRES: self.getThreshold()
        }
        return out

    @abstractmethod
    def policyType(self):
        pass

    @abstractmethod
    def isConcrete(self):
        pass

    @abstractmethod
    def deepCopy(self):
        pass

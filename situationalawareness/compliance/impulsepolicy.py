from situationalawareness.compliance.policy import Policy
from situationalawareness.comprehensionstage import TCONST

class ImpulsePolicy(Policy):
    def __init__(self, threshold: float):
        super().__init__(threshold)

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def policyType(self):
        return TCONST.TYPE_IMP

    def isConcrete(self):
        return True

    def deepCopy(self):
        t = self.getThreshold()
        id = self.getPolicyID()
        p = ImpulsePolicy(t)
        p.threshold = t
        p.policyID = id
        return p
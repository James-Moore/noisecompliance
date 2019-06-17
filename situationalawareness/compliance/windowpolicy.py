import json
from situationalawareness.compliance.policy import Policy
from situationalawareness.comprehensionstage import TCONST

class WindowPolicy(Policy):
    def __init__(self, threshold: float, seconds: int):
        super().__init__(threshold)
        self.windowSize = seconds

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def getWindowSize(self):
        return self.windowSize

    def toDict(self):
        out = super().toDict()
        out.update({TCONST.WIN_SIZE: self.getWindowSize()})
        return out

    def policyType(self):
        return TCONST.TYPE_WIN

    def isConcrete(self):
        return True

    def deepCopy(self):
        t = self.getThreshold()
        id = self.getPolicyID()
        winsize = self.getWindowSize()
        p = WindowPolicy(t, winsize)
        p.threshold = t
        p.policyID = id
        return p
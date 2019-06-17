from situationalawareness.comprehensionstage.impulsetracker import ImpulseTracker
from situationalawareness.comprehensionstage.situation import Situation
from situationalawareness.comprehensionstage.movingaverage import MovingAverage
from situationalawareness.perceptionstage.environment import Environment
from situationalawareness.compliance.policies import Policies

class Comprehension:
    def __init__(self, policies : Policies, enviroment: Environment):
        self.situation = Situation(policies, enviroment)

    def comprehendSituation(self, policies: Policies, environment: Environment):
        self.getSituation().update(policies, environment)
        self.getSituation().printSummary()

    def getSituation(self):
        return self.situation
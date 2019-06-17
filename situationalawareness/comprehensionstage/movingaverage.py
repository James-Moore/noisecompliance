class MovingAverage:

    def __init__(self):
        self.count = 0
        self.average = 0

    def __deepcopy__(self, memodict={}):
        return self.deepCopy()

    def getAverage(self):
        return self.average

    def update(self, value):
        if (self.count == 0):
            self.count = 1
            self.averag = value
        else:
            self.count += 1
            differential = (value - self.average) / self.count
            newAverage = self.average + differential
            self.average = newAverage

    def deepCopy(self):
        copy = MovingAverage()
        copy.count = self.count
        copy.average = self.average
        return copy
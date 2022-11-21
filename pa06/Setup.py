import random
import math

class Setup:
    def __init__(self):
        self.aType = 0
        self.DELTA = 0
        self.alpha = 0
        self.Dx = 0

    def setVariables(self, parameters):
        self.aType = parameters['aType']
        self.DELTA = parameters['delta']
        self.alpha = parameters['alpha']
        self.Dx = parameters['dx']

    def getAType(self):
        return self.aType

    def getDELTA(self):
        return self.DELTA

    def getAlpha(self):
        return self.alpha

    def getDx(self):
        return self.Dx

import random
import math

class Setup:
    def __init__(self):
        self._aType = 0
        self._DELTA = 0
        self._alpha = 0
        self._Dx = 0
        self._resolution = 0

    def setVariables(self, parameters):
        self._aType = parameters['aType']
        self._DELTA = parameters['delta']
        self._alpha = parameters['alpha']
        self._Dx = parameters['dx']
        self._resolution = parameters['resolution']

    def getAType(self):
        return self._aType

    def getDELTA(self):
        return self._DELTA

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._Dx

from Setup import *

class HillClimbing(Setup):
    def __init__(self):
        super().__init__()
        self.LIMIT_STUCK = 100

    def getLIMIT_STUCK(self):
        return self.LIMIT_STUCK

    def run(self):
        pass

class SteepestAscent(HillClimbing):
    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.solution = current
        p.value = valueC

    def bestOf(self, neighbors, p):
        Valuelist = []
        for i in range(len(neighbors)):
            mucurrent = neighbors[i]
            Valuelist.append(p.evaluate(mucurrent))

        bestValue = min(Valuelist)
        bestindex = Valuelist.index(bestValue)
        best = neighbors[bestindex]
        return best, bestValue

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")

class FirstChoice(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)

        i = 0
        while i < self.LIMIT_STUCK:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        p.solution = current
        p.value = valueC

    def displaySetting(self):
        DELTA = self.getDELTA()  # Numeric 클래스에서 DELTA 변수 호출하여 사용
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        print("Mutation step size:", DELTA)

class GradientDescent(HillClimbing):
    def run(self,p):
        CurrentP = p.randomInit()
        valueC = p.evaluate(CurrentP)

        while True:
            nextP = p.takeStep(CurrentP, valueC)
            valueN = p.evaluate(nextP)

            if valueN >= valueC:
                break
            else:
                CurrentP = nextP
                valueC = valueN

        p.solution = CurrentP
        p.value = valueC


    def displaySetting(self):
        print()
        print("Search algorithm: Gradient descent")
        print()
        print("Update rate: ", self.alpha)
        print("Increment for calculating derivatives: ", self.Dx)

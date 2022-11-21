from Setup import *

class Optimizer(Setup):
    def __init__(self):
        super().__init__()
        self.pType = 0
        self.numExp = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self.pType = parameters['pType']
        self.numExp = parameters['numExp']

    def getNumExp(self):
        return self.numExp

    def displayNumExp(self):
        print()
        print('Number of experiments: ', self.numExp)

    def displaySetting(self):
        if self.pType == 1 and self.aType != 4 and self.aType != 6:
            print("Mutation step size: ", self.DELTA)


class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__()
        self.pType = 0
        self.LIMIT_STUCK = 100
        self.numExp = 0
        self.numRestart = 0

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self.pType = parameters['pType']
        self.LIMIT_STUCK = parameters['limitStuck']
        self.numExp = parameters['numExp']
        self.numRestart = parameters['numRestart']

    def getLIMIT_STUCK(self):
        return self.LIMIT_STUCK

    def getNumExp(self):
        return self.numExp

    def displayNumExp(self):
        print()
        print('Number of experiments: ', self.numExp)

    def displaySetting(self):
        print()
        if self.pType == 1:
            print("Mutation step size: ", self.DELTA)

    def run(self, p):
        pass

    def randomRestart(self, p):
        i = 1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        while i < self.numRestart:
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval += p.getNumEval()
            if newMinimum < bestMinimum:
                bestSolution = newSolution
                bestMinimum = newMinimum
            i += 1
        p.storeResult(bestSolution, bestMinimum)


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
        current = p.randomInit()
        valueC = p.evaluate(current)
        LIMIT_STUCK = self.getLIMIT_STUCK()

        i = 0
        num = 1
        f = open('first.txt', 'w')
        while i < LIMIT_STUCK:
            f.writelines(str(valueC) + ',' + str(num) + '\n')
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
            num += 1
        f.close()
        p.storeResult(current, valueC)

    def displaySetting(self):
        DELTA = self.getDELTA()  # Numeric 클래스에서 DELTA 변수 호출하여 사용
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        print("Mutation step size:", DELTA)
        print("Max evaluations with no improvement:", self.LIMIT_STUCK, "iterations")

class Stochastic(HillClimbing):
    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self.LIMIT_STUCK:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS >= valueC:
                i += 1
            else:
                current = successor
                valueC = valueS
                i = 0
        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s:
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

    def displaySetting(self):
        print()
        print("Search algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

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

        p.storeResult(CurrentP, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient descent")
        print()
        print("Update rate: ", self.alpha)
        print("Increment for calculating derivatives: ", self.Dx)


class MetaHeuristics(Optimizer):
    def __init__(self):
        super().__init__()
        self.limitEval = 0
        self.numSample = 100
        self.whenBestFound = 0

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self.pType = parameters['pType']
        self.LIMIT_STUCK = parameters['limitStuck']
        self.numExp = parameters['numExp']
        self.numRestart = parameters['numRestart']
        self.limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self.whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self.limitEval))

    def run(self):
        pass


class SimulatedAnnealing(MetaHeuristics):
    def run(self, p):
        limitEval = self.limitEval
        CurrentP = p.randomInit()
        valueC = p.evaluate(CurrentP)
        best, valueBest = CurrentP, valueC
        whenBestFound = i = 1
        T = self.initTemp(p)
        num = 1
        f = open('annealing.txt', 'w')
        while True:
            f.writelines(str(valueC) + ',' + str(num) + '\n')
            T = self.tSchedule(T)
            if T == 0 or i == limitEval:
                break
            nextP = p.randomMutant(CurrentP)
            valueN = p.evaluate(nextP)
            i += 1
            dE = valueN - valueC
            if dE < 0:
                CurrentP = nextP
                valueC = valueN
            elif math.exp(-dE / T) >= random.random():
                CurrentP = nextP
                valueC = valueN
            if valueC < valueBest:
                (best, valueBest) = (CurrentP, valueC)
                whenBestFound = i
            num += 1
        f.close()
        self.whenBestFound = whenBestFound
        p.storeResult(best, valueBest)

    def initTemp(self, p):
        diffs = []
        for i in range(self.numSample):
            c0 = p.randomInit()
            v0 = p.evaluate(c0)
            c1 = p.randomMutant(c0)
            v1 = p.evaluate(c1)
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self.numSample
        t = dE / math.log(2)
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10 ** 4))

    def displaySetting(self):
        print()
        print("Search algorithm: Stimulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)
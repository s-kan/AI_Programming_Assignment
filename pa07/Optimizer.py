from Setup import *

class Optimizer(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0
        self._numExp = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print('Number of experiments: ', self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:
            print("Mutation step size: ", self._DELTA)


class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__()
        self._pType = 0
        self._LIMIT_STUCK = 100
        self._numExp = 0
        self._numRestart = 0

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._LIMIT_STUCK = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']

    def getLIMIT_STUCK(self):
        return self._LIMIT_STUCK

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print('Number of experiments: ', self._numExp)

    def displaySetting(self):
        print()
        if self._pType == 1:
            print("Mutation step size: ", self._DELTA)

    def run(self, p):
        pass

    def randomRestart(self, p):
        i = 1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        while i < self._numRestart:
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
        while i < LIMIT_STUCK:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)


    def displaySetting(self):
        DELTA = self.getDELTA()
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        print()
        print("Mutation step size:", DELTA)
        print("Max evaluations with no improvement:", self._LIMIT_STUCK, "iterations")

class Stochastic(HillClimbing):
    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._LIMIT_STUCK:
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
        print("Update rate: ", self._alpha)
        print("Increment for calculating derivatives: ", self._Dx)


class MetaHeuristics(Optimizer):
    def __init__(self):
        super().__init__()
        self._limitEval = 0
        self.whenBestFound = 0

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._LIMIT_STUCK = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self._limitEval))

    def run(self):
        pass


class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        super().__init__()
        self._numSample = 100

    def run(self, p):
        CurrentP = p.randomInit()  # current값 정의
        valueC = p.evaluate(CurrentP)  # current value 정의
        best, valueBest = CurrentP, valueC
        whenBestFound = i = 1
        T = self.initTemp(p)
        while True:
            T = self.tSchedule(T)
            if T == 0 or i == self._limitEval:
                break
            nextP = p.randomMutant(CurrentP)
            valueN = p.evaluate(nextP)
            i += 1
            dE = valueN - valueC
            if dE < 0:
                CurrentP = nextP
                valueC = valueN
            elif math.exp(-dE / T) > random.uniform(0, 1):
                CurrentP = nextP
                valueC = valueN
            if valueC < valueBest:
                (best, valueBest) = (CurrentP, valueC)
                whenBestFound = i
        self._whenBestFound = whenBestFound
        p.storeResult(best, valueBest)

    def initTemp(self, p):
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()
            v0 = p.evaluate(c0)
            c1 = p.randomMutant(c0)
            v1 = p.evaluate(c1)
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample
        t = dE / math.log(2)
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10 ** 4))

    def displaySetting(self):
        print()
        print("Search algorithm: Stimulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)

class GA(MetaHeuristics):
    def __init__(self):
        super().__init__()
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        MetaHeuristics.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._resolution = parameters['resolution']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def run(self, p):
        pop = p.initializePop(
            self._popSize)  # [ [evaluatedvalue1,[chromosome1]], ... , [evaluatedvalueN,[chromosomeN]] ]
        best = self.evalAndFindBest(pop, p)
        nEval = p.getNumEval()
        whenBestFound = nEval
        while nEval < self._limitEval:
            newPop = []
            i = 0
            while i < self._popSize:
                par1, par2 = self.selectParents(pop)
                ch1, ch2 = p.crossover(par1, par2, self._pC)
                newPop.extend([ch1, ch2])
                i += 2
            newPop = [p.mutation(ind, self._pM) for ind in newPop]
            pop = newPop
            newBest = self.evalAndFindBest(pop, p)
            nEval = p.getNumEval()
            if newBest[0] < best[0]:
                best = newBest
                whenBestFound = nEval
        self._whenBestFound = whenBestFound
        bestSolution = p.indToSol(best)
        p.storeResult(bestSolution, best[0])

    def evalAndFindBest(self, pop, p):
        best = pop[0]
        p.evalInd(best)
        bestValue = best[0]
        for i in range(1, len(pop)):
            p.evalInd(pop[i])
            newValue = pop[i][0]
            if newValue < bestValue:
                best = pop[i]
                bestValue = newValue
        return best

    def selectParents(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1, ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1, ind2)
        return par1, par2

    def selectTwo(self, pop):  # 랜덤하게 pop 중 두개를 고르는 역할
        popCopy = pop[:]
        random.shuffle(popCopy)
        return popCopy[0], popCopy[1]

    def binaryTournament(self, ind1, ind2):
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        MetaHeuristics.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

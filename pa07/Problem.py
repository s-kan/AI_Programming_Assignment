from Setup import *

class Problem(Setup):
    def __init__(self):
        super().__init__()
        self._solution = []
        self._value = 0
        self._NumEval = 0
        self._bestSolution = []
        self._bestMinimum = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._sumOfNumEval = 0
        self._avgWhen = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pFileName = parameters['pFileName']

    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self, current):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    def getSolution(self):
        return self._solution

    def getValue(self):
        return self._value

    def getNumEval(self):
        return self._NumEval

    def storeExpResult(self, results):
        self._bestSolution = results[0]
        self._bestMinimum = results[1]
        self._avgMinimum = results[2]
        self._avgNumEval = results[3]
        self._sumOfNumEval = results[4]
        self._avgWhen = results[5]

class Numeric(Problem):
    def __init__(self):
        super().__init__()
        self._expression = ""
        self._domain = []

    def setVariables(self, parameters):
        Problem.setVariables(self, parameters)
        infile = open(self._pFileName, 'r')
        varNames = []
        low = []
        up = []
        domain_t = []

        self._expression = infile.readline().rstrip()
        domainlist = infile.readlines()

        for i in domainlist:
            domain_t.append(i[:-1])
        for i in range(0, len(domain_t)):
            a = domain_t[i]
            b = a.split(",")
            varNames.append(b[0])
            b[1] = float(b[1])
            low.append(b[1])
            b[2] = float(b[2])
            up.append(b[2])

        self._domain.append(varNames)
        self._domain.append(low)
        self._domain.append(up)

        infile.close()

    def randomInit(self):
        domain = self._domain
        init = []
        for i in range(len(domain[1])):
            l = domain[1][i]
            h = domain[2][i]
            init.append(random.uniform(l, h))
        return init

    def evaluate(self, current):
        self._NumEval += 1
        expr = self._expression
        varNames = self._domain[0]

        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutants(self, current):
        c1 = current[:]
        c2 = current[:]
        m1 = []
        m2 = []
        for i in range(len(self._domain[0])):
            c1 = self.mutate(current, i, self._DELTA)
            m1.append(c1)
        for i in range(len(self._domain[0])):
            c2 = self.mutate(current, i, self._DELTA * -1)
            m2.append(c2)

        neighbors = m1 + m2
        return neighbors

    def randomMutant(self, current):  ###
        domain = self._domain
        length = len(domain[0])
        i = random.randint(0, length - 1)
        d = random.choice([self._DELTA, (self._DELTA * -1)])
        return self.mutate(current, i, d)

    def mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain
        l = domain[1][i]  # Lower bound of i-th
        u = domain[2][i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def takeStep(self, x, v):  # nextP 만드는 함수
        grad = self.gradient(x, v)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self._alpha * grad[i]
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self._Dx
            g = (self.evaluate(xCopyH) - v) / self._Dx
            grad.append(g)

        return grad

    def isLegal(self, xCopy):
        domain = self._domain
        l = domain[1]
        u = domain[2]

        for i in range(len(domain[0])):
            if l[i] <= xCopy[i] <= u[i]:
                return True
            else:
                return False

    def initializePop(self, size):  # Make a population of given size
        pop = []
        for i in range(size):
            chromosome = self.randBinStr()
            pop.append([0, chromosome])
        return pop

    def randBinStr(self):
        k = len(self._domain[0]) * self._resolution
        chromosome = []
        for i in range(k):
            allele = random.randint(0, 1)
            chromosome.append(allele)
        return chromosome

    def evalInd(self, ind):  # ind: [fitness, chromosome]
        ind[0] = self.evaluate(self.decode(ind[1]))  # Record fitness

    def decode(self, chromosome):
        r = self._resolution
        low = self._domain[1]  # list of lower bounds
        up = self._domain[2]  # list of upper bounds
        genotype = chromosome[:]
        phenotype = []
        start = 0
        end = r  # The following loop repeats for # variables
        for var in range(len(self._domain[0])):
            value = self.binaryToDecimal(genotype[start:end],
                                         low[var], up[var])
            phenotype.append(value)
            start += r
            end += r
        return phenotype

    def binaryToDecimal(self, binCode, l, u):
        r = len(binCode)
        decimalValue = 0
        for i in range(r):
            decimalValue += binCode[i] * (2 ** (r - 1 - i))
        return l + (u - l) * decimalValue / 2 ** r

    def crossover(self, ind1, ind2, uXp):
        # pC is interpreted as uXp# (probability of swap)
        chr1, chr2 = self.uXover(ind1[1], ind2[1], uXp)
        return [0, chr1], [0, chr2]

    def uXover(self, chrInd1, chrInd2, uXp):  # uniform crossover
        chr1 = chrInd1[:]  # Make copies
        chr2 = chrInd2[:]
        for i in range(len(chr1)):
            if random.uniform(0, 1) < uXp:
                chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2

    def mutation(self, ind, mrF):  # bit-flip mutation
        # pM is interpreted as mrF (factor to adjust mutation rate)
        child = ind[:]  # Make copy
        n = len(ind[1])
        for i in range(n):
            if random.uniform(0, 1) < mrF * (1 / n):
                child[1][i] = 1 - child[1][i]
        return child

    def indToSol(self, ind):
        return self.decode(ind[1])

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))


    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        print("Average number of evaluations:", self._avgNumEval)
        print()
        print("Best solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self._bestMinimum))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)  # Convert the list to a tuple

class Tsp(Problem):
    def __init__(self):
        super().__init__()
        self._numCities = 0
        self._locations = []
        self._distanceTable = []

    def setVariables(self, parameters):
        Problem.setVariables(self, parameters)
        infile = open(self._pFileName, 'r')
        # First line is number of cities
        self._numCities = int(infile.readline())
        locs = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locs.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self._locations = locs
        self._distanceTable = self.calcDistanceTable()

    def calcDistanceTable(self):
        import numpy as np

        numCities = self._numCities
        locations = self._locations

        v = []
        d = []
        a1arr = []
        a2arr = []
        b1arr = []
        b2arr = []
        carr = []
        for i in range(numCities):
            v.append(locations[i])

        for i in range(numCities):
            a1 = v[i][0]
            a1arr.append(a1)
            a2 = v[i][1]
            a2arr.append(a2)
        b1arr = list(a1arr)
        b2arr = list(a2arr)

        for i in range(numCities):
            for j in range(numCities):
                c = (((b1arr[j] - a1arr[i]) ** 2) + (b2arr[j] - a2arr[i]) ** 2) ** 0.5
                carr.append(c)

        table = np.array(carr).reshape(numCities, numCities)
        return table

    def randomInit(self):
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        self._NumEval += 1

        dtable = self._distanceTable
        cost = 0
        for i in range(self._numCities - 1):
            a = current[i]
            b = current[i + 1]
            cost += dtable[a][b]
        return cost

    def randomMutant(self, current):  # Apply inversion
        while True:
            i, j = sorted([random.randrange(self._numCities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def initializePop(self, size):  # Make a population of given size
        n = self._numCities  # n: number of cities
        pop = []
        for i in range(size):
            chromosome = self.randomInit()
            pop.append([0, chromosome])
        return pop

    def evalInd(self, ind):  # ind: [fitness, chromosome]
        ind[0] = self.evaluate(ind[1])  # Record fitness

    def crossover(self, ind1, ind2, XR):
        # pC is interpreted as XR (crossover rate)
        if random.uniform(0, 1) <= XR:
            chr1, chr2 = self.oXover(ind1[1], ind2[1])
        else:
            chr1, chr2 = ind1[1][:], ind2[1][:]  # No change
        return [0, chr1], [0, chr2]

    def oXover(self, chrInd1, chrInd2):  # Ordered Crossover
        chr1 = chrInd1[:]
        chr2 = chrInd2[:]  # Make copies
        size = len(chr1)
        a, b = sorted([random.randrange(size) for _ in range(2)])
        holes1, holes2 = [True] * size, [True] * size
        for i in range(size):
            if i < a or i > b:
                holes1[chr2[i]] = False
                holes2[chr1[i]] = False
        # We must keep the original values somewhere
        # before scrambling everything
        temp1, temp2 = chr1, chr2
        k1, k2 = b + 1, b + 1
        for i in range(size):
            if not holes1[temp1[(i + b + 1) % size]]:
                chr1[k1 % size] = temp1[(i + b + 1) % size]
                k1 += 1
            if not holes2[temp2[(i + b + 1) % size]]:
                chr2[k2 % size] = temp2[(i + b + 1) % size]
                k2 += 1
        # Swap the content between a and b (included)
        for i in range(a, b + 1):
            chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2

    def mutation(self, ind, mR):  # mutation by inversion
        # pM is interpreted as mR (mutation rate for inversion)
        child = ind[:]  # Make copy
        if random.uniform(0, 1) <= mR:
            i, j = sorted([random.randrange(self._numCities)
                           for _ in range(2)])
            child[1] = self.inversion(child[1], i, j)
        return child

    def indToSol(self, ind):
        return ind[1]

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        print("Average number of evaluations:", self._avgNumEval)
        print()
        print("Best order of visits:")
        self.tenPerRow(self._bestSolution)  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._bestMinimum)))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    def tenPerRow(self, solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

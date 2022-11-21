from Setup import *

class Problem(Setup):
    def __init__(self):
        super().__init__()  # DELTA, alpha, dx
        self.solution = []
        self.value = 0
        self.NumEval = 0
        self.bestSolution = []
        self.bestMinimum = 0
        self.avgMinimum = 0
        self.avgNumEval = 0
        self.sumOfNumEval = 0
        self.avgWhen = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self.pFileName = parameters['pFileName']

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
        self.solution = solution
        self.value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self.NumEval))

    def getSolution(self):
        return self.solution

    def getValue(self):
        return self.value

    def getNumEval(self):
        return self.NumEval

    def storeExpResult(self, results):
        self.bestSolution = results[0]
        self.bestMinimum = results[1]
        self.avgMinimum = results[2]
        self.avgNumEval = results[3]
        self.sumOfNumEval = results[4]
        self.avgWhen = results[5]

class Numeric(Problem):
    def __init__(self):
        super().__init__()
        self.expression = ""
        self.domain = []

    def setVariables(self, parameters):
        Problem.setVariables(self, parameters)
        infile = open(self.pFileName, 'r')
        varNames = []
        low = []
        up = []
        domain_t = []

        self.expression = infile.readline().rstrip()
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

        self.domain.append(varNames)
        self.domain.append(low)
        self.domain.append(up)

        infile.close()

    def randomInit(self):
        domain = self.domain
        init = []
        for i in range(len(domain[1])):
            l = domain[1][i]
            h = domain[2][i]
            init.append(random.uniform(l, h))
        return init

    def evaluate(self, current):
        self.NumEval += 1
        expr = self.expression
        varNames = self.domain[0]

        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutants(self, current):
        c1 = current[:]
        c2 = current[:]
        m1 = []
        m2 = []
        for i in range(len(self.domain[0])):
            c1 = self.mutate(current, i, self.DELTA)
            m1.append(c1)
        for i in range(len(self.domain[0])):
            c2 = self.mutate(current, i, self.DELTA * -1)
            m2.append(c2)

        neighbors = m1 + m2
        return neighbors

    def randomMutant(self, current):  ###
        domain = self.domain
        length = len(domain[0])
        i = random.randint(0, length - 1)
        d = random.choice([self.DELTA, (self.DELTA * -1)])
        return self.mutate(current, i, d)

    def mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self.domain
        l = domain[1][i]  # Lower bound of i-th
        u = domain[2][i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def takeStep(self, x, v):  # nextP 만드는 함수
        grad = self.gradient(x, v)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self.alpha * grad[i]
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self.Dx
            g = (self.evaluate(xCopyH) - v) / self.Dx
            grad.append(g)

        return grad

    def isLegal(self, xCopy):
        domain = self.domain
        l = domain[1]
        u = domain[2]

        for i in range(len(domain[0])):
            if l[i] <= xCopy[i] <= u[i]:
                return True
            else:
                return False

    def describe(self):
        print()
        print("Objective function:")
        print(self.expression)   # Expression
        print("Search space:")
        varNames = self.domain[0]
        low = self.domain[1]
        up = self.domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))


    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self.avgMinimum))
        print("Average number of evaluations:", self.avgNumEval)
        print()
        print("Best solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self.bestMinimum))
        print()
        print("Total number of evaluations: {0:,}".format(self.NumEval))

    def coordinate(self):
        c = [round(value, 3) for value in self.solution]
        return tuple(c)  # Convert the list to a tuple

class Tsp(Problem):
    def __init__(self):
        super().__init__()
        self.numCities = 0
        self.locations = []
        self.distanceTable = []

    def setVariables(self, parameters):
        Problem.setVariables(self, parameters)
        infile = open(self.pFileName, 'r')
        # First line is number of cities
        self.numCities = int(infile.readline())
        locs = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locs.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.locations = locs
        self.distanceTable = self.calcDistanceTable()

    def calcDistanceTable(self):
        import numpy as np

        numCities = self.numCities
        locations = self.locations

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
        n = self.numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        self.NumEval += 1

        dtable = self.distanceTable
        cost = 0
        for i in range(self.numCities - 1):
            a = current[i]
            b = current[i + 1]
            cost += dtable[a][b]
        return cost

    def randomMutant(self, current):  # Apply inversion
        while True:
            i, j = sorted([random.randrange(self.numCities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def mutants(self, current):
        n = self.numCities
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

    def describe(self):
        print()
        n = self.numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self.locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self.avgMinimum))
        print("Average number of evaluations:", self.avgNumEval)
        print()
        print("Best order of visits:")
        self.tenPerRow(self.bestSolution)  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self.bestMinimum)))
        print()
        print("Total number of evaluations: {0:,}".format(self.NumEval))

    def tenPerRow(self, solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

import random
from Setup import *

class Problem(Setup):
    def __init__(self):
        super().__init__()
        self.solution = []
        self.NumEval = 0
        self.value = 0

    def setVariables(self):
        pass

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

class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self.expression = ""
        self.domain = []

    def setVariables(self):
        fileName = input("Enter the file name of a function:")
        infile = open(fileName, 'r')
        self.expression = str(infile.readline().rstrip())
        v_n = []
        low = []
        upper = []
        line = infile.readline().rstrip()
        while line != '':
            l = list(line.split(','))
            v_n.append(l[0])
            low.append(float(l[1]))
            upper.append(float(l[2]))
            line = infile.readline().rstrip()
        infile.close()
        self.domain = [v_n, low, upper]

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
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self.value))
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

    def setVariables(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        self.numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.locations = locations
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
        print("Best order of visits:")
        self.tenPerRow(self.solution)  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self.value)))
        print()
        print("Total number of evaluations: {0:,}".format(self.NumEval))

    def tenPerRow(self, solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

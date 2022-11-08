import random
import math

DELTA = 0.01  # Mutation step size
LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement
NumEval = 0  # Total number of evaluations

def main:

class problem:
    def firstChoice(self, p):
        current = Numeric.randomInit(p)  # 'current' is a list of values
        valueC = Numeric.evaluate(current, p)
        i = 0
        while i < LIMIT_STUCK:
            successor = self.randomMutant(current, p)
            valueS = Numeric.evaluate(successor, p)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        return current, valueC

    def randomMutant(self, current, p):  ###
        domain = p[1]
        length = len(domain[1])
        i = random.randint(0, length - 1)
        d = random.choice([DELTA, (DELTA * -1)])
        return Numeric.mutate(current, i, d, p)


class Numeric(problem):
    def createProblem(self):
        fileName = input("Enter the file name of a function:")
        infile = open(fileName, 'r')
        expression = str(infile.readline().rstrip())
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
        domain = [v_n, low, upper]
        return expression, domain

    def randomInit(self, p):  ###
        domain = p[1]
        init = []
        for i in range(len(domain[1])):
            l = domain[1][i]
            h = domain[2][i]
            init.append(random.uniform(l, h))
        return init

    def evaluate(self, current, p):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        global NumEval

        NumEval += 1
        expr = p[0]  # p[0] is function expression
        varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutate(current, i, d, p):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = p[1]  # [VarNames, low, up]
        l = domain[1][i]  # Lower bound of i-th
        u = domain[2][i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describeProblem(self, p):
        print()
        print("Objective function:")
        print(p[0])  # Expression
        print("Search space:")
        varNames = p[1][0]  # p[1] is domain: [VarNames, low, up]
        low = p[1][1]
        up = p[1][2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        print()
        print("Mutation step size:", DELTA)

    def displayResult(self, solution, minimum):
        print()
        print("Solution found:")
        print(self.coordinate(solution))  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(minimum))
        print()
        print("Total number of evaluations: {0:,}".format(NumEval))

    def coordinate(self, solution):
        c = [round(value, 3) for value in solution]
        return tuple(c)

class First_choice(Numeric):
    def firstChoice(self, p):
        current = Numeric.randomInit(p)  # 'current' is a list of values
        valueC = Numeric.evaluate(current, p)
        i = 0
        while i < LIMIT_STUCK:
            successor = self.randomMutant(current, p)
            valueS = Numeric.evaluate(successor, p)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        return current, valueC

    def randomMutant(self, current, p):  ###
        domain = p[1]
        length = len(domain[1])
        i = random.randint(0, length - 1)
        d = random.choice([DELTA, (DELTA * -1)])
        return Numeric.mutate(current, i, d, p)

class Steepest_ascent(Numeric):
    def steepestAscent(self, p):
        current = Numeric.randomInit(p)  # 'current' is a list of values
        valueC = Numeric.evaluate(current, p)
        while True:
            neighbors = self.mutants(current, p)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        return current, valueC

    def mutants(self, current, p):  ###
        c1 = current[:]
        c2 = current[:]
        m1 = []
        m2 = []
        for i in range(len(p[1][0])):
            c1 = Numeric.mutate(current, i, DELTA, p)
            m1.append(c1)
        for i in range(len(p[1][0])):
            c2 = Numeric.mutate(current, i, DELTA * -1, p)
            m2.append(c2)

        neighbors = m1 + m2
        return neighbors

    def bestOf(self, neighbors, p):  ###
        V = []
        for i in range(len(neighbors)):
            mucurrent = neighbors[i]
            V.append(self.evaluate(mucurrent, p))

        bestValue = min(V)
        bestindex = V.index(bestValue)
        best = neighbors[bestindex]
        return best, bestValue


class Tsp(problem):
    def createProblem(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        table = self.calcDistanceTable(self, numCities, locations)
        return numCities, locations, table

    def calcDistanceTable(self, numCities, locations):  ###
        import numpy as np
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

    def randomInit(self, p):  # Return a random initial tour
        n = p[0]
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current, p):  ###
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        global NumEval

        NumEval += 1

        dtable = p[2]
        cost = 0
        for i in range(p[0] - 1):
            a = current[i]
            b = current[i + 1]
            cost += dtable[a][b]
        return cost

    def inversion(self, current, i, j):  # Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describeProblem(self, p):
        print()
        n = p[0]
        print("Number of cities:", n)
        print("City locations:")
        locations = p[1]
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")

    def displayResult(self, solution, minimum):
        print()
        print("Best order of visits:")
        self.tenPerRow(solution)  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(minimum)))
        print()
        print("Total number of evaluations: {0:,}".format(NumEval))

    def tenPerRow(self, solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

main()
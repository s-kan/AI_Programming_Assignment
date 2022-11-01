import random
import math

NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table


def calcDistanceTable(numCities, locations): ###
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
    return table # A symmetric matrix of pairwise distances


def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init


def evaluate(current, p): ###
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


def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy

def bestOf(neighbors, p): ###
    V = []
    for i in range(len(neighbors)):
        mucurrent = neighbors[i]
        V.append(evaluate(mucurrent, p))

    bestValue = min(V)
    bestindex = V.index(bestValue)
    best = neighbors[bestindex]
    return best, bestValue

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()

main()

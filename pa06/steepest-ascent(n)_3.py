from Problem import Numeric


def main():
    p = Numeric()
    p.setVariables()
    steepestAscent(p)
    p.describe()
    displaySetting(p)
    p.report()


def steepestAscent(p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS

    p.storeResult(current, valueC)


def bestOf(neighbors, p):
    ###
    Valuelist = []
    for i in range(0, len(neighbors)):
        mucurrent = neighbors[i]
        Valuelist.append(p.evaluate(mucurrent))

    bestValue = min(Valuelist)
    bestindex = Valuelist.index(bestValue)
    best = neighbors[bestindex]
    return best, bestValue


def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")


main()
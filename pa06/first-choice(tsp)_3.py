from Problem import Tsp

def main():
    p = Tsp()
    p.setVariables()
    firstChoice(p)
    p.describe()
    displaySetting()
    p.report()


def firstChoice(p):
    current = p.randomInit()
    valueC = p.evaluate(current)

    LIMIT_STUCK = 100
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS  #
            i = 0
        else:
            i += 1

    p.storeResult(current, valueC)


def displaySetting(p):
    DELTA = p.getDELTA()
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

main()


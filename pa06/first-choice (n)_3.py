from Problem import Numeric

def main():
    p = Numeric()
    p.setVariables()
    firstChoice(p)
    p.describe()
    displaySetting(p)
    p.report()

def firstChoice(p):
    current = p.randomInit()
    valueC = p.evaluate(current)

    i = 0
    while i < p.LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0
        else:
            i += 1
    p.solution = current
    p.value = valueC

def displaySetting(p):
    DELTA = p.getDELTA()
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)
main()

from Problem import Numeric

def main():
    p = Numeric()
    p.createProblem()
    steepestAscent(p)
    p.describeProblem()
    p.displaySetting()
    p.displayResult()

def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.solution = current
    p.value = valueC


def bestOf(neighbors, p):
    Valuelist = []
    for i in range(len(neighbors)):
        mucurrent = neighbors[i]
        Valuelist.append(p.evaluate(mucurrent))

    bestValue = min(Valuelist)
    bestindex = Valuelist.index(bestValue)
    best = neighbors[bestindex]
    return best, bestValue

main()
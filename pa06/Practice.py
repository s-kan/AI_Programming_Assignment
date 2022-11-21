import Problem
import math

def main():
    p = Problem.Numeric()
    print(initTemp(p))

def initTemp(p):
    numSample = 5
    diffs = []
    for i in range(numSample):
        c0 = p.randomInit()
        v0 = p.evaluate(c0)
        c1 = p.randomMutant(c0)
        v1 = p.evaluate(c1)
        diffs.append(abs(v1 - v0))
    dE = sum(diffs) / numSample
    t = dE / math.log(2)
    return t

main()
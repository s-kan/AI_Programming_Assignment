from Problem import *
from HillClimbing import *

def main():
    p, ptype = selectProblem()
    a = selectAlgorithm(ptype)
    a.run(p)
    p.describe()
    a.displaySetting()
    p.report()

def selectProblem():
    print("Select the problem type:")
    print("  1. Numberical Optimization")
    print("  2. TSP")
    t = int(input("Enter the number: "))
    if t == 1:
        p = Numeric()
    else:
        p = Tsp()
    p.setVariables()
    return p, t

def selectAlgorithm(ptype):
    if ptype == 1:
        print()
        print("Select the search algorithm: ")
        print(" 1. Steepest-Ascent")
        print(" 2. First-Choice")
        print(" 3. Gradient Descent")
        while (1):
            atype = int(input("Enter the number: "))
            if atype == 1 or atype == 2 or atype == 3:
                break
            else:
                continue
    else:
        print()
        print("Select the search algorithm: ")
        print(" 1. Steepest-Ascent")
        print(" 2. First-Choice")
        while(1):
            atype = int(input("Enter the number: "))
            if atype == 1 or atype == 2:
                break
            else:
                continue
    if atype == 1:
        return SteepestAscent()
    elif atype == 2:
        return FirstChoice()
    elif atype == 3:
        return GradientDescent()

main()
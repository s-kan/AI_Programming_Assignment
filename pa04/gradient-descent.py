from Problem import Numeric

def main():
    p = Numeric()
    p.createProblem()
    gradientDscent(p)
    p.describeProblem()
    displaySetting(p)
    p.displayResult()

def gradientDscent(p):
    CurrentP = p.randomInit()
    valueC = p.evaluate(CurrentP)

    while True:
        nextP = p.takeStep(CurrentP, valueC)
        valueN = p.evaluate(nextP)

        if valueN >= valueC:
            break
        else:
            CurrentP = nextP
            valueC = valueN

    p.solution = CurrentP
    p.value = valueC

def displaySetting(p):
    print()
    print("Search algorithm: Gradient descent")
    print()
    print("Update rate: ", p.getAlpha())
    print("Increment for calculating derivatives: ", p.getDx())


main()
from Problem import Numeric

DELTA = 0.01   # Mutation step size
LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
    p = Numeric()
    p.createProblem()
    firstChoice(p)
    p.describeProblem()
    p.displaySetting()
    p.displayResult()

def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)

    i = 0
    while i < p.LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.solution = current
    p.value = valueC

main()

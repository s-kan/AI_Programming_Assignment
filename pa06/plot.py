import matplotlib.pyplot as plt

def main():
    plotting()

def plotting():
    file1 = open('first.txt','r')
    file2 = open('annealing.txt', 'r')

    pieces1 = []
    pieces2 = []

    line1 = file1.readline()
    while line1 != '':
        pieces1.append(eval(line1))
        line1 = file1.readline()
    file1.close()

    line2 = file2.readline()
    while line2 != '':
        pieces2.append(eval(line2))
        line2 = file2.readline()
    file2.close()

    x1 = []
    y1 = []
    for i in range(len(pieces1)):
        x1.append(pieces1[i][1])
        y1.append(pieces1[i][0])
    x2 = []
    y2 = []
    for i in range(len(pieces2)):
        x2.append(pieces2[i][1])
        y2.append(pieces2[i][0])

    plt.figure()
    plt.plot(x1, y1, label = "Frist-Choice HC")
    plt.plot(x2, y2, label = "Simulated Annealing")
    plt.legend()
    plt.title('Search Performance (TSP-100)')
    plt.xlabel('Number of Evaluationis')
    plt.ylabel('Tour Cost')
    plt.savefig('pa06')
    plt.show()

main()
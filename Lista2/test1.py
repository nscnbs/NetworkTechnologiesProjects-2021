import networkx as nx
import matplotlib.pyplot as plt
from numpy import linspace
from main import test1, przepustowosc, przeplyw, T


G = nx.disjoint_union(nx.cycle_graph(9), nx.cycle_graph(11))
for i in range(9):
    G.add_edge(i, i + 10)


N = [
    [0, 2, 3, 2, 9, 2, 1, 6, 9, 6, 3, 4, 5, 7, 3, 5, 2, 9, 6, 9],
    [1, 0, 9, 2, 8, 8, 4, 5, 2, 6, 6, 5, 5, 2, 7, 3, 8, 6, 4, 3],
    [8, 1, 0, 8, 5, 5, 4, 1, 4, 6, 2, 5, 4, 7, 4, 2, 9, 4, 3, 3],
    [8, 5, 7, 0, 4, 9, 9, 2, 4, 7, 3, 2, 3, 7, 8, 8, 9, 5, 9, 7],
    [9, 1, 1, 7, 0, 6, 6, 9, 1, 4, 1, 7, 4, 5, 9, 5, 8, 5, 3, 5],
    [4, 4, 6, 1, 9, 0, 5, 6, 2, 8, 2, 8, 9, 6, 2, 6, 4, 1, 1, 3],
    [5, 4, 2, 7, 8, 3, 0, 8, 4, 3, 6, 8, 9, 7, 1, 7, 2, 2, 9, 3],
    [1, 1, 2, 5, 4, 5, 2, 0, 2, 6, 3, 3, 1, 5, 5, 4, 6, 1, 4, 9],
    [5, 5, 8, 1, 9, 6, 7, 2, 0, 1, 4, 2, 3, 9, 8, 7, 2, 2, 1, 6],
    [7, 4, 8, 2, 3, 2, 8, 1, 6, 0, 7, 7, 6, 4, 8, 8, 6, 9, 9, 6],
    [3, 6, 9, 3, 1, 9, 3, 2, 5, 8, 0, 7, 8, 7, 9, 7, 3, 1, 2, 4],
    [8, 1, 3, 5, 4, 9, 3, 5, 3, 2, 7, 0, 3, 7, 3, 2, 6, 6, 7, 4],
    [1, 5, 2, 8, 5, 9, 4, 8, 7, 6, 7, 8, 0, 9, 3, 7, 3, 8, 2, 8],
    [2, 8, 2, 7, 5, 8, 9, 5, 9, 1, 4, 5, 8, 0, 9, 9, 4, 8, 8, 7],
    [8, 6, 9, 6, 6, 2, 6, 5, 3, 1, 9, 4, 9, 5, 0, 4, 2, 2, 2, 3],
    [7, 3, 8, 7, 4, 1, 4, 5, 3, 9, 9, 3, 2, 7, 2, 0, 7, 9, 5, 6],
    [7, 7, 8, 8, 7, 5, 4, 4, 8, 3, 5, 6, 5, 1, 1, 5, 0, 9, 1, 6],
    [8, 7, 2, 2, 3, 7, 6, 9, 6, 6, 3, 1, 2, 9, 8, 9, 2, 0, 8, 9],
    [4, 9, 2, 1, 7, 3, 6, 2, 5, 1, 7, 6, 5, 7, 7, 5, 4, 4, 0, 8],
    [1, 9, 8, 6, 4, 3, 6, 1, 8, 8, 5, 3, 4, 1, 2, 6, 4, 3, 4, 0],
]

przeplyw(G, N)
przepustowosc(G, N)

suma = sum(sum(r) for r in N)
min_Tmax = [T(G, suma, m) for m in range(1, 11)]

# print('checkpoint before loop')

for m in range(10, 0, -2):
    startT = min_Tmax[m - 1]
    print("m: ", m)
    print("T początkowe: ", startT)
    for p in linspace(0.9, 0.99, num=5):
        print("p: ", p)
        plt.figure()
        plt.imshow([
                test1(G, N, Tmax, p, m, step=100)
                for Tmax in linspace(startT, 10*startT, num=5)
            ],
            extent=[0, 1000, startT, 10*startT],
            aspect="auto",
            origin="lower",
        )
        plt.colorbar()
        plt.ylabel("T_max")
        plt.xlabel("Liczba dodanych pakietów przy p={}, m={}".format(p, m))
        plt.savefig("TEST1_{}_{}.png".format(m, p))
        plt.close()
        # print("done as TEST1_{}_{}.png".format(m, p))

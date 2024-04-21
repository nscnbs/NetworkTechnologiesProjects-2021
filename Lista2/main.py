import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from copy import deepcopy


def przepustowosc(graf, macierz):
    nx.set_edge_attributes(graf, 0, "c")
    for i, j in graf.edges:
        graf[i][j]["c"] = graf[i][j]["a"] // 5 * 50 + 50


def przeplyw(graf, macierz):
    nx.set_edge_attributes(graf, 0, "a")
    wezly = nx.number_of_nodes(graf)
    for i in range(wezly):
        for j in range(wezly):
            path = nx.shortest_path(graf, i, j)
            for n in range(len(path) - 1):
                graf[path[n]][path[n + 1]]["a"] += macierz[i][j]


def T(graf, sum_macierz, m):
    T = 0
    for i, j in graf.edges:
        a = graf[i][j]["a"]
        c = graf[i][j]["c"]
        if a >= c / m:
            return None
        else:
            T += a / (c / m - a)
    return T / sum_macierz


def niezawodnosc(graf, macierz, T_max, p, m, iterations=100, intervals=10):
    s = 0
    sum_macierz = sum(sum(row) for row in macierz)
    t_podstaw = T(graf, sum_macierz, m)
    for _ in range(iterations):
        p_graf = deepcopy(graf)
        for _ in range(intervals):
            usun = [e for e in nx.edges(p_graf) if random.random() > p]
            if usun:
                p_graf.remove_edges_from(usun)
                if not nx.is_connected(p_graf):
                    break
                przeplyw(p_graf, macierz)
                t = T(p_graf, sum_macierz, m)
            else:
                t = t_podstaw
            if not t or t >= T_max:
                break
            s += 1
    return s / (iterations * intervals)


def szybki_przeplyw(graf, i, j, step):
    path = nx.shortest_path(graf, i, j)
    for n in range(len(path) - 1):
        graf[path[n]][path[n + 1]]["a"] += step


def test1(graf, macierz, T_max, p, m, iterations=10, step=10):
    t_graf = deepcopy(graf)
    t_macierz = deepcopy(macierz)
    results = [niezawodnosc(t_graf, t_macierz, T_max, p, m)]
    for _ in range(iterations):
        while True:
            i, j = random.randint(0, 19), random.randint(0, 19)
            if i != j:
                break
        t_macierz[i][j] += step
        szybki_przeplyw(t_graf, i, j, step)
        results.append(niezawodnosc(t_graf, t_macierz, T_max, p, m))
    print("Niezawodność:", results[0])
    return results


def test2(graf, macierz, T_max, p, m, iterations=10):
    t_graf = deepcopy(graf)
    results = [niezawodnosc(t_graf, macierz, T_max, p, m)]
    for _ in range(iterations):
        for i, j in t_graf.edges:
            t_graf[i][j]["c"] += 50
        results.append(niezawodnosc(t_graf, macierz, T_max, p, m))
    print("Niezawodność:", results)
    return results


def test3(graf, macierz, T_max, p, m, iterations=10):
    t_graf = deepcopy(graf)
    results = [niezawodnosc(t_graf, macierz, T_max, p, m)]
    caps = nx.get_edge_attributes(t_graf, "c").values()
    new_cap = sum(caps) / len(caps)
    non_nodes = list(nx.non_edges(t_graf))
    for _ in range(iterations):
        i, j = random.sample(non_nodes, 1)[0]
        non_nodes.remove((i, j))
        t_graf.add_edge(i, j)
        t_graf[i][j]["c"] = new_cap
        przeplyw(t_graf, macierz)
        results.append(niezawodnosc(t_graf, macierz, T_max, p, m))
    print("Niezawodność:", results)
    return results


def main():
    G = nx.disjoint_union(nx.cycle_graph(9), nx.cycle_graph(11))
    for i in range(9):
        G.add_edge(i, i + 10)

    N = []
    for i in range(20):
        N.append([])
        for j in range(20):
            if i == j:
                N[i].append(0)
            else:
                N[i].append(random.randint(1, 9))
    print(np.matrix(N))
    print()

    przeplyw(G, N)
    przepustowosc(G, N)

    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, font_size=6, rotate=False)
    nx.draw_networkx_labels(G, pos, font_color="w")
    plt.show()


if __name__ == "__main__":
    main()

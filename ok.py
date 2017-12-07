from random import randint
from networkx import nx
import matplotlib.pyplot as plt
from math import ceil
from copy import deepcopy

def hypergraphe():
    nbr_sommets = randint(4, 15)
    hyper_aretes = randint(2, round((3/4)*nbr_sommets))

    sommets = []
    for i in range(1, nbr_sommets + 1): sommets.append(i)
    copie = deepcopy(sommets)

    G = [[] for i in range(hyper_aretes + 1)]
    nbr_sommets_hyper = ceil(nbr_sommets / hyper_aretes)

    d = 0
    for h_a in G:
        c = randint(1, nbr_sommets_hyper)
        b = []
        for j in range(c + 1):
            if randint(0, 4) != 1 or (j == c and not h_a):
                a = randint(0, nbr_sommets-1)
                while a in b:
                    a = randint(0, nbr_sommets-1)
                b.append(a)
                h_a.append(sommets[a])
                d += 1
                if sommets[a] in copie: del copie[copie.index(sommets[a])]

    if copie:
        for i in copie: G.append(i)
    return G, nbr_sommets

def graph_incidence(graph):
    pos = {}
    G = nx.Graph()
    ite = 0
    for i in range(len(graph)):
        if type(graph[i]) == list:  # Hyperarêtes
            x = "E{}".format(i+1)
            G.add_node(x)
            pos[x] = (-10, -20*(i*2))
            for j in graph[i]:
                if j not in nx.nodes(G):
                    G.add_node(j)
                    pos[j] = (10, -20*(i+1+ite))
                    ite += 1
                G.add_edge(j, x)
        else:       # Singleton
            G.add_node(graph[i])
            pos[graph[i]] = (10, -20*(i+1+ite))
    plt.subplot(121)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()

def graph_primal(graph):
    graphP = nx.Graph()
    for i in range(len(graph)):
        if type(graph[i]) == list:
            graphP.add_node(graph[i][0])
            if len(graph[i]) > 1:
                for sommet in range(len(graph[i])):
                    graphP.add_node(graph[i][sommet])
                    for autre_sommet in range(len(graph[i])):
                        if sommet != autre_sommet:
                            graphP.add_edge(graph[i][sommet], graph[i][autre_sommet])
        else:
            graphP.add_node(graph[i])
    plt.subplot(121)
    nx.draw(graphP ,with_labels=True, font_weight='bold')
    plt.show()

def constru_incidence(G, nbr_sommets):
    G_inci = {i+1 : [] for i in range(nbr_sommets)}
    for i in range(len(G)):
        if type(G[i]) == list:
            h_a = "E{}".format(i+1)
            G_inci[h_a] = G[i]
            for j in G[i]:
                G_inci[j].append(h_a)
    return G_inci

def constru_primal(graph, nbr_sommets):
    gPrimal = {i+1 : [] for i in range(nbr_sommets)}
    for hyper_arete in graph:
        if type(hyper_arete) == list:
            for sommet in hyper_arete :
                for i in hyper_arete:
                    if i not in gPrimal[sommet] and i != sommet:
                        gPrimal[sommet].append(i)
    return gPrimal

def dfs(graph, node, cycle, visited):
    cycle[0].append(node)
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, cycle, visited)
            cycle[0].pop()
    else :
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) \
            and cycle[0][-1] in cycle[0][:-1]:
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return visited, cycle

def cycle(graph):
    done = []
    cycle = [[]]
    visited = []
    for node in graph:
        if node not in done and len(graph[node])>1:
            cycle[0] = []
            visited, cycle = dfs(graph, node, cycle, visited)
            for i in visited:
                done.append(i)
    return cycle[1:]

def acyclique_Berge(graph):
    res = False
    if cycle(graph):
        res = True
    return res

def cordal(graph, nbr_sommets):
    gPrimal = constru_primal(graph, nbr_sommets)
    all_cycle = cycle(gPrimal)
    print(all_cycle)
    res = True
    for current_cycle in all_cycle:
        nbrSommetCycle = len(current_cycle)
        if nbrSommetCycle >= 4:
            res = False
            for i in range(nbrSommetCycle):
                voisin_G = i-1
                voisin_D = i-1
                if voisin_D >= nbrSommetCycle:
                    voisin_D = 0
                for j in range(nbrSommetCycle):
                    if j != voisin_G and j != voisin_D and j != i :
                        if current_cycle[j] in gPrimal[current_cycle[i]]:
                            res = True
    return res

if __name__ == "__main__":
    graph, nbr_sommets = hypergraphe()
    G_inci = constru_incidence(graph, nbr_sommets)
    print(acyclique_Berge(G_inci))
    graph_incidence(graph)
    print(cordal(graph, nbr_sommets))
    graph_primal(graph)

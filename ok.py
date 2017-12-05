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
                for sommet in range(1,len(graph[i])):
                    graphP.add_node(graph[i][sommet])
                    graphP.add_edge(graph[i][sommet], graph[i][sommet-1])
                graphP.add_edge(graph[i][-1], graph[i][0])
        else:
            graphP.add_node(graph[i])
    plt.subplot(121)
    nx.draw_circular(graphP ,with_labels=True, font_weight='bold')
    plt.show()

def constru(G, nbr_sommets):
    G_inci = {i+1 : [] for i in range(nbr_sommets)}
    for i in range(len(G)):
        if type(G[i]) == list:
            h_a = "E{}".format(i+1)
            G_inci[h_a] = G[i]
            for j in G[i]:
                G_inci[j].append(h_a)
    return G_inci

def dfs(graph, node, visited, cycle):
    cycle.append(node)
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, visited, cycle)
            cycle.pop()
    else :
        if len(cycle)>2 and not(cycle[-1] == cycle[-3]) and cycle[-1] in cycle[:-1]:
            print('cycle : ' + str(cycle))
    return visited

if __name__ == "__main__":
    global visited
    visited = []
    graph, nbr_sommets = hypergraphe()
    G_inci = constru(graph, nbr_sommets)
    print(G_inci)
    visited = []
    for node in G_inci:
        if not(node in visited) and len(G_inci[node])>1:
            visited = []
            cycle = []
            visited = dfs(G_inci, node, visited, cycle)
    graph_incidence(graph)

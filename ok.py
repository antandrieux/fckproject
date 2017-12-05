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

def constru_incidence(G, nbr_sommets):
    G_inci = {i+1 : [] for i in range(nbr_sommets)}
    for i in range(len(G)):
        if type(G[i]) == list:
            h_a = "E{}".format(i+1)
            G_inci[h_a] = G[i]
            for j in G[i]:
                G_inci[j].append(h_a)
    return G_inci

def dfs(graph, node, cycle, visited = []):
    cycle[0].append(node)
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, cycle, visited)
            cycle[0].pop()
    else :
<<<<<<< HEAD
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) and cycle[0][-1] in cycle[0][:-1]:
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return visited, cycle
=======
<<<<<<< HEAD
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) and cycle[0][-1] in cycle[0][:-1]:
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return visited, cycle
=======
        if len(cycle)>2 and not(cycle[-1] == cycle[-3]) and cycle[-1] in cycle[:-1]:
            print('cycle : ' + str(cycle[cycle.index(cycle[-1]):-1]))
    return visited
>>>>>>> 7ceadeffff0ce9dbc8bfa048d3cd87d0be5f50db
>>>>>>> d0cddf9694a1687845dee9e8065718fb48464b65

def cycle(graph):
    done = []
    cycle = [[]]
    for node in G_inci:
        if not(node in done) and len(graph[node])>1:
            done = []
            cycle[0] = []
            are_done, cycle = dfs(graph, node, cycle)
            for i in are_done:
                done.append(i)
    return cycle[1:]

if __name__ == "__main__":
    graph, nbr_sommets = hypergraphe()
<<<<<<< HEAD
    G_inci = constru_incidence(graph, nbr_sommets)
=======
<<<<<<< HEAD
    print(graph)
    G_inci = constru_incidence(graph, nbr_sommets)
=======
    G_inci = constru(graph, nbr_sommets)
>>>>>>> 7ceadeffff0ce9dbc8bfa048d3cd87d0be5f50db
>>>>>>> d0cddf9694a1687845dee9e8065718fb48464b65
    print(G_inci)
    print(cycle(G_inci))
    graph_incidence(graph)

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
    return G

def graph_incidence(graph):
    G = nx.Graph()
    for i in range(len(graph)):
        if type(graph[i]) == list:  # Hyperarêtes
            x = "E{}".format(i+1)
            G.add_node(x)
            for j in graph[i]:
                G.add_node(j)
                G.add_edge(j, x)
        else:       # Singleton
            G.add_node(graph[i])
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
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
    nx.draw(graphP, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    graph = hypergraphe()
    print(graph)
    #graph_incidence(graph)
    graph_primal(graph)


graph = {
    'E1' : ['v1','v2', 'v3'],
    'E2' : ['v2', 'v3'],
    'E3' : ['v3', 'v5', 'v6'],
    'E4' : ['v4'],
    'v1' : ['E1'],
    'v2' : ['E2', 'E3'],
    'v3' : ['E1', 'E2', 'E3'],
    'v4' : ['E4'],
    'v5' : ['E3'],
    'v6' : ['E3'],
    'v7' : []

}

def dfs(graph,node, visited = []):
    if node in visited:
        print('cycle')
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
    return visited
print(dfs(graph,'E1'))

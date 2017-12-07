from random import randint
from networkx import nx
import matplotlib.pyplot as plt
from math import ceil
from copy import deepcopy

def hypergraphe():
    nbr_sommets = randint(4, 15)
    hyper_aretes = randint(2, round((1/2)*nbr_sommets))

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
            if randint(0, 3) != 1 or (j == c and not h_a):
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
    '''

    '''
    pos = {}
    G = nx.Graph()
    ite = 0
    for i in range(len(graph)):
        if type(graph[i]) == list:  # Hyperarêtes
            x = "E{}".format(i+1)
            G.add_node(x)
            # Création de la position du noeud dans l'affichage
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

def bron(r,p,x, gPrimal):
    '''
    Application de l'algorithme de Bron-Kerbosch -- Backtracking
    '''
    if len(p) == 0 and len(x) == 0:
        CLIQUES_MAX.append(r)
        return
    for sommet in p[:]: # Copie
        new_r = r[::]
        new_r.append(sommet)
        # graph_primal[sommet] == voisins de sommet
        new_p = [val for val in p if val in gPrimal[sommet]] # p intersecte graph_primal[sommet]
        new_x = [val for val in x if val in gPrimal[sommet]] # x intersecte graph_primal[sommet]
        bron(new_r,new_p,new_x, gPrimal)
        p.remove(sommet)
        x.append(sommet)

def alpha_cyclique(gPrimal, graph):
    '''
    Vérifie si le graphe primal est acyclique.
    '''
    global CLIQUES_MAX
    CLIQUES_MAX = []    # Liste de toutes les cliques maximales
    bron([], [val + 1 for val in range(len(gPrimal))], [], gPrimal)
    i = 0
    cliques_ha = True
    # Vérifie si les cliques maximales correspondent à des hyper-aretes
    while i < len(CLIQUES_MAX) and cliques_ha:
        if CLIQUES_MAX[i] not in graph:
            cliques_ha = False
        i += 1
    if cordal(graph_primal) and cliques_ha:
        print("Le graphe est alpha-acyclique")
    else:
        print("Le graphe n'est pas alpha-acyclique")

def dfs(graph, node, cycle, visited = []):
    cycle[0].append(node)
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, cycle, visited)
            cycle[0].pop()
    else :
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) and cycle[0][-1] in cycle[0][:-1]:
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return cycle

def cycle(graph):
    cycle = [[]]
    visited = []
    for node in graph:
        if  len(graph[node])>1:
            cycle[0] = []
            visited = []
            cycle = dfs(graph, node, cycle, visited)
    return cycle[1:]

def acyclique_Berge(graph):
    res = True
    if cycle(graph):
        res = False
    return res

def cordal(gPrimal):
    all_cycle = cycle(gPrimal)
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
    if not acyclique_Berge(G_inci):
        print("Le graphe n'est pas acyclique au sens de Berge.")
        alpha_cyclique(constru_primal(graph, nbr_sommets), graph)
    else:
        print("Le graphe est acyclique au sens de Berge.")
    graph_incidence(graph)
    graph_primal(graph)

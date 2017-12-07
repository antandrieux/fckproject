'''
AUTHOR = Antoine Andrieux
Matricule = 000443686
B-INFO

AUTHOR = Loukas Wets
Matricule =
'''
'''
INFO-F203 – Algorithmique 2
Projet : "Cycles et hypergraphes"
'''

from random import randint
from networkx import nx
import matplotlib.pyplot as plt
from math import ceil
from copy import deepcopy

def gene_hypergraph():
    '''
    Génération aléatoire d'un hyper-graphe composé de sommets et d'hyper-aretes
    '''
    nbr_sommets = randint(4, 15)
    hyper_aretes = randint(2, round((1/2)*nbr_sommets))

    sommets = []
    for i in range(1, nbr_sommets + 1): sommets.append(i)
    copie = deepcopy(sommets)

    G = [[] for i in range(hyper_aretes)]
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
        h_a.sort()
    if copie:
        for i in copie: G.append(i)
    return G, nbr_sommets

def show_incident(graph):
    '''
    Affiche le graphe d'incidence à l'aide des librairies NetworkX et MatPlotLib
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
    '''
    Construit et retourne le graphe d'incidence sous forme d'un dictionnaire.
    '''
    gInci = {i+1 : [] for i in range(nbr_sommets)}
    for i in range(len(G)):
        if type(G[i]) == list:
            # Chaque hyper-arete en clé vers une liste contenant les sommets qui y sont reliées
            h_a = "E{}".format(i+1)
            gInci[h_a] = G[i]
            # Chaque sommet en clé vers une liste contenant les hyper-aretes qui y sont reliées
            for j in G[i]:
                gInci[j].append(h_a)
    return gInci

def constru_primal(graph, nbr_sommets):
    gPrimal = {i+1 : [] for i in range(nbr_sommets)}
    for hyper_arete in graph:
        if type(hyper_arete) == list:
            for sommet in hyper_arete :
                for i in hyper_arete:
                    if i not in gPrimal[sommet] and i != sommet:
                        gPrimal[sommet].append(i)
    return gPrimal

def detect_cliques_max(r,p,x, gPrimal):
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
        detect_cliques_max(new_r,new_p,new_x, gPrimal)
        p.remove(sommet)
        x.append(sommet)

def alpha_acyclique(gPrimal, graph):
    '''
    Vérifie si le graphe primal est acyclique.
    '''
    global CLIQUES_MAX
    CLIQUES_MAX = []    # Liste de toutes les cliques maximales
    detect_cliques_max([], [val + 1 for val in range(len(gPrimal))], [], gPrimal)
    i = 0
    cliques_ha = True
    # Vérifie si les cliques maximales correspondent à des hyper-aretes
    while i < len(CLIQUES_MAX) and cliques_ha:
        print(CLIQUES_MAX[i])
        # Verifie pour les hyper-aretes et Singletons
        if CLIQUES_MAX[i] not in graph and CLIQUES_MAX[i][0] not in graph:
            cliques_ha = False
        i += 1
    if detect_cordal(gPrimal) and cliques_ha:
        print("Le graphe est alpha-acyclique")
    else:
        print("Le graphe n'est pas alpha-acyclique")

def dfs(g, node, cycle, visited):
    cycle[0].append(node)
    if node not in visited:
        visited.append(node)
        for n in g[node]:
            dfs(g, n, cycle, visited)
            cycle[0].pop()
    else :
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) \
        and cycle[0][-1] in cycle[0][:-1]:
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return cycle

def detect_cycle(g):
    cycle = [[]]
    visited = []
    for node in g:
        if  len(g[node])>1:
            cycle[0] = []
            visited = []
            cycle = dfs(g, node, cycle, visited)
    return cycle[1:]

def acyclique_Berge(gInci):
    res = True
    if detect_cycle(gInci):
        res = False
    return res

def detect_cordal(gPrimal):
    all_cycle = detect_cycle(gPrimal)
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

def hypercycle(graph):
    '''
    Affiche si le graphe est acyclique au sens de Berge.
    '''
    gInci = constru_incidence(graph, nbr_sommets)
    if not acyclique_Berge(gInci):
        print("Le graphe n'est pas acyclique au sens de Berge.")
        alpha_acyclique(constru_primal(graph, nbr_sommets), graph)
    else:
        print("Le graphe est acyclique au sens de Berge.")

if __name__ == "__main__":
    graph, nbr_sommets = gene_hypergraph()
    #graph, nbr_sommets = [[1,2,3],[1,5],[3,5,6],[4], 7], 7
    hypercycle(graph)
    show_incident(graph)

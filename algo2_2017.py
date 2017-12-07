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

def show_incidence(graph):
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

def constru_incidence(G, nbr_sommets):
<<<<<<< HEAD
    '''
    Construit et retourne le graphe d'incidence sous forme d'un dictionnaire.
    '''
=======
<<<<<<< HEAD
    '''
    Construit et retourne le graphe d'incidence sous forme d'un dictionnaire.
    '''
=======
<<<<<<< HEAD:algo2_2017.py
    '''
    Construit et retourne le graphe d'incidence sous forme d'un dictionnaire.
    '''
=======
    """Construit un dictionaire ou les indices sont les sommets
        et hyper-aretes du graphe d'incidence et les valeurs, les
        sommets et hyper-aretes aux quels ils sont reliés.
    """
>>>>>>> fe2994892c39bea04dc77d235fa5476c1df187f5:clique_max.py
>>>>>>> d078032ee5cb3f8712932d00f702329634177663
>>>>>>> 92b499df543132fee9238b736bfcc7348e07f31e
    gInci = {i+1 : [] for i in range(nbr_sommets)}
    for i in range(len(G)):
        if type(G[i]) == list:
            # Chaque hyper-arete en clé et
            # en valeur, une liste contenant les sommets qui y sont reliées
            h_a = "E{}".format(i+1)
            gInci[h_a] = G[i]
            # Chaque sommet en clé et
            # en valeur, une liste contenant les hyper-aretes qui y sont reliées
            for j in G[i]:
                gInci[j].append(h_a)
    return gInci

def constru_primal(graph, nbr_sommets):
    '''
    Construit un dictionaire ou les indices sont les sommets
    du graphe primal et les valeurs, les sommets aux quels
    ils sont reliés.
    '''
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
    '''
    Parcours en profondeur d'un graphe et trouve les cycles et
    renvoie les cycles trouvés.
    '''
    cycle[0].append(node)    #cycle[0] designe le chemin courant dans le graphe.
    if node not in visited:
        visited.append(node)
        for voisin in g[node]:
            dfs(g, voisin, cycle, visited)
            cycle[0].pop()
    else :
        if len(cycle[0])>2 and not(cycle[0][-1] == cycle[0][-3]) \
        and cycle[0][-1] in cycle[0][:-1]:       #Determine s'il y a une cycle.
            cycle.append(cycle[0][cycle[0].index(cycle[0][-1]):-1])
    return cycle

def detect_cycle(g):
    '''
    Renvoie tout les cycles du graphe g.
    '''
    cycle = [[]]
    visited = []
    for node in g:
        if  len(g[node])>1: #si len(g[node])<1 il n'est pas possible d avoir
            cycle[0] = []   #un cycle.
            visited = []
            cycle = dfs(g, node, cycle, visited)
    return cycle[1:]

def acyclique_Berge(gInci):
    '''
    Renvoie True si le graphe gInci est acyclique au sens berge
    False si non.
    '''
    res = True
    if detect_cycle(gInci):
        res = False
    return res

<<<<<<< HEAD
=======
<<<<<<< HEAD
def detect_cordal(gPrimal):
    all_cycle = detect_cycle(gPrimal)
=======
<<<<<<< HEAD:algo2_2017.py
>>>>>>> 92b499df543132fee9238b736bfcc7348e07f31e
def detect_cordal(gPrimal):
    '''
    Renvoie True si le graphe gPprimal est cordale
    False si non.
    '''
    all_cycle = detect_cycle(gPrimal)         #Listes des cycles de gPrimal.
<<<<<<< HEAD
=======
>>>>>>> fe2994892c39bea04dc77d235fa5476c1df187f5:clique_max.py
>>>>>>> d078032ee5cb3f8712932d00f702329634177663
>>>>>>> 92b499df543132fee9238b736bfcc7348e07f31e
    res = True
    for current_cycle in all_cycle:            #Parcours des cycles du graph.
        nbrSommetCycle = len(current_cycle)
        if nbrSommetCycle >= 4:
            res = False
            for i in range(nbrSommetCycle):
                voisin_G = i-1                  #voisins gauche et droite du
                voisin_D = i-1                  #sommet a l indice i.
                if voisin_D >= nbrSommetCycle:
                    voisin_D = 0
                for j in range(nbrSommetCycle):
                    if j != voisin_G and j != voisin_D and j != i :
                        if current_cycle[j] in gPrimal[current_cycle[i]]:
                            #determine si il y a une corde dans le cycle.
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD:algo2_2017.py
>>>>>>> d078032ee5cb3f8712932d00f702329634177663
>>>>>>> 92b499df543132fee9238b736bfcc7348e07f31e
        print("Le graphe est acyclique au sens de Berge.")

if __name__ == "__main__":
    graph, nbr_sommets = gene_hypergraph()
    #graph, nbr_sommets = [[1,2,3],[1,5],[3,5,6],[4], 7], 7
    hypercycle(graph)
<<<<<<< HEAD
    show_incidence(graph)
    graph_incidence(graph)
=======
    show_incident(graph)
<<<<<<< HEAD
=======
=======
        print("Le graphe est acyclique au sens de Berge et par conséquent alpha-acyclique")
    graph_incidence(graph)
    graph_primal(graph)
>>>>>>> fe2994892c39bea04dc77d235fa5476c1df187f5:clique_max.py
>>>>>>> d078032ee5cb3f8712932d00f702329634177663
>>>>>>> 92b499df543132fee9238b736bfcc7348e07f31e

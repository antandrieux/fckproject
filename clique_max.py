def bron(r,p,x):
    '''
    Application de l'algorithme de Bron-Kerbosch -- Backtracking
    '''
    if len(p) == 0 and len(x) == 0:
        cliques_max.append(r)
        return
    for sommet in p[:]: # Copie
        new_r = r[::]
        new_r.append(sommet)
        # graph_primal[sommet] == voisins de sommet
        new_p = [val for val in p if val in graph_primal[sommet]] # p intersecte graph_primal[sommet]
        new_x = [val for val in x if val in graph_primal[sommet]] # x intersecte graph_primal[sommet]
        bron(new_r,new_p,new_x)
        p.remove(sommet)
        x.append(sommet)

def alpha_cyclique(graph_primal, graph):
    '''
    Vérifie si le graphe primal est acyclique.
    '''
    global cliques_max
    cliques_max = []    # Liste de toutes les cliques maximales
    bron([], [val + 1 for val in range(len(graph_primal))], [])
    i = 0
    cliques_ha = True
    # Vérifie si les cliques maximales correspondent à des hyper-aretes
    while i < len(cliques_max) and cliques_ha:
        if cliques_max[i] not in graph:
            cliques_ha = False
        i += 1
    # cordal =
    if cordal and cliques_ha:
        print("Le graphe est alpha-acyclique")
    else:
        print("Le graphe n'est pas alpha-acyclique")

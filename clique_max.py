graph_primal = {1:[2,4], 2:[1, 4], 3:[], 4:[1, 2]}

def bron(r,p,x):
    if len(p) == 0 and len(x) == 0:
        cliques_max.append(r)
        return
    for sommet in p[:]:
        new_r = r[::]
        new_r.append(sommet)
        new_p = [val for val in p if val in graph_primal[sommet]] # p intersects N(sommet)
        new_x = [val for val in x if val in graph_primal[sommet]] # x intersects N(sommet)
        bron(new_r,new_p,new_x)
        p.remove(sommet)
        x.append(sommet)

def alpha_cyclique(graph_primal, G_inci):
    global cliques_max
    cliques_max = []
    bron([], [val + 1 for val in range(len(graph_primal))], [])
    i = 0
    cliques_ha = True
    while i < len(cliques_max) and cliques_ha:
        if cliques_max[i] not in G_inci.values():
            cliques_ha = False
        i += 1
    # cordal =
    if cordal and cliques_ha:
        print("Le graphe est alpha-acyclique")
    else:
        print("Le graphe n'est pas alpha-acyclique")

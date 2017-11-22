from random import randint, shuffle
from networkx import nx
import matplotlib as plt
from math import ceil

if __name__ == "__main__":
    nbr_sommets = randint(1, 15)
    hyper_aretes = round((3/4)*nbr_sommets)
    sommets = []
    for i in range(1, nbr_sommets+1): sommets.append(i)
    shuffle(sommets)
    copie = sommets
    G = [[] for i in range(hyper_aretes + 1)]
    nbr_sommets_hyper = ceil(nbr_sommets / hyper_aretes)
    d = 0
    for h_a in G:
        b = randint(0, 1)
        c = randint(1, nbr_sommets_hyper)
        for j in range(c+1):
            if b == 1:
                h_a.append(sommets[0])
                d += 1
                if sommets[0] in copie: del copie[0]
    if sommets:
        for i in sommets: G.append(i)

    print(G)

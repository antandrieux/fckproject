from random import randint
from networkx import nx
import matplotlib as plt
from math import ceil
from copy import deepcopy

if __name__ == "__main__":
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

    print(G)

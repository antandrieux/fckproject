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
    'v7' : [],

}

graph_primal = {}
for elem in graph:
    if type(elem) == list:
        if elem2 in graph_primal:

    else :
        graph_primal[elem] = []

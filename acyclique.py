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

def dfs(graph,node, visited = []):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
    else :
        print('cycle')
    return visited
print(dfs(graph,'v1'))

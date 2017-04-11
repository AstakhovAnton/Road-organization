import networkx as nx
import random
g = nx.DiGraph()
n = int(input())
for i in range(n):
    g.add_node(i)
for i in range(3 * n):
    a = random.randint(0, n - 1)
    b = random.randint(0, n - 1)
    g.add_edge(a, b, weight=random.randint(1, 10))
for i in range(10):
    print(nx.degree(g, 1, i))
#print("The shortest path between 1 and 2:")
#print(*nx.dijkstra_path(g, 1, 2))
for i in range(n):
    print(i,  ":", end = " ")
    print(g.neighbors(i))
#print()
#print(nx.degree(g, 1))
MG=nx.MultiGraph()
MG.add_weighted_edges_from([(1,2,.5), (1,2,.75), (2,3,.5)])
MG.degree(weight='weight')
GG=nx.Graph()
for n,nbrs in MG.adjacency_iter():
    for nbr,edict in nbrs.items():
        minvalue=min([d['weight'] for d in edict.values()])
        GG.add_edge(n,nbr, weight = minvalue)
nx.shortest_path(GG,1,3)
import networkx
import matplotlib.pyplot as plt

G=networkx.Graph()
e=[('a','b',0.3),('b','c',0.9),('a','c',0.5),('c','d',1.2)]
G.add_weighted_edges_from(e)
print(G.nodes())
print(networkx.dijkstra_path(G,'a','d'))

networkx.draw(G)
plt.show()



Q=networkx.cubical_graph()
lollipop=networkx.lollipop_graph(10,20)

networkx.draw_circular(Q)
plt.show()
networkx.draw_spectral(lollipop)
plt.show()

networkx.draw(Q)   # тип по умолчанию spring_layout
networkx.draw(Q,pos=networkx.spectral_layout(Q), nodecolor='r',edge_color='b')
plt.show()

S = networkx.path_graph(4)
cities = {0: "Toronto", 1: "London", 2: "Berlin", 3: "New York"}

H = networkx.relabel_nodes(S, cities)

print("Nodes of graph: ")
print(H.nodes())
print("Edges of graph: ")
print(H.edges())
networkx.draw(H)

plt.show()
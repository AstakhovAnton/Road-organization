import networkx as nx

class Network:
    def __init__(self):
        self.matrix = nx.Graph()
    def add_node(self, name):
        self.matrix.add_node(name)
    def add_edge(self, name1, name2, w):
        self.matrix.add_edge(name1, name2, weight=w)
    def remove_node(self, name):
        self.matrix.remove_node(name)
    def remove_edge(self, name1, name2, w):
        self.matrix.remove_edge(name1, name2)


import networkx as nx
from Road import Road
from Car import Car
size = 50

class Network:
    def __init__(self):
        self.matrix = nx.Graph()
        self.mat_object = [[0] * size] * size

    def add_node(self, name):
        self.matrix.add_node(name)

    def add_edge(self, name1, name2, w, listx, listy):
        self.matrix.add_edge(name1, name2, weight=w)
        self.mat_object[name1][name2] = Road(listx, listy)

    def remove_node(self, name):
        self.matrix.remove_node(name)
    def remove_edge(self, name1, name2, w):
        self.matrix.remove_edge(name1, name2)

if __name__ == '__main__':
    mynet = Network()
    for i in range(1, 4):
        mynet.add_node(i)
    mynet.add_edge(1, 2, 3, (1, 2), (1, 2))
    mynet.add_edge(1, 3, 1, (1, 2), (1, 2))
    mynet.add_edge(3, 2, 1, (1, 2), (1, 2))
    mycar = Car(1)
    mycar.movement(mynet)
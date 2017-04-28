import time
import networkx as nx
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint
inf = 10 ** 6

class Point:
    def __init__(self, abs, ord):
        self.abs = abs
        self.ord = ord

    def x(self):
        return(self.abs)

    def y(self):
        return(self.ord)

    def QPoint(self):
        return QPoint(self.abs, self.ord)

    @staticmethod
    def dist(point1, point2):
        return (((point2.x() - point1.x()) ** 2 + (point2.y() - point1.y()) ** 2) ** 0.5)

class Car:
    def __init__(self, v, drawer, start, finish):
        self.velocity = v
        self.current_vertex = start
        self.finish_vertex = finish
        self.drawer = drawer

    def way(self, net):
        #for name in net.matrix.nodes():
        #    print(name, ":", end=" ")
        #    print(net.matrix.neighbors(name))
        return (nx.dijkstra_path(net.matrix, self.current_vertex, self.finish_vertex))[1]

    def movement(self, net):
        #print('Прибыл в', self.current_vertex)
        time.sleep(1/self.velocity)
        if self.current_vertex == self.finish_vertex:
            return

        where = self.way(net)
        best_len = inf
        best_road = 0
        for road in net.matrix[self.current_vertex][where].keys():
            if net.matrix[self.current_vertex][where][road]['weight'] < best_len:
                best_len = net.matrix[self.current_vertex][where][road]['weight']
                best_road = road

        for i in range(len(net.matrix[self.current_vertex][where][best_road]['dots'])):
            time.sleep(1/self.velocity)
            self.current_point = net.matrix[self.current_vertex][where][best_road]['dots'][i]
            self.drawer.objpoint = Point(self.current_point[0], self.current_point[1])
            self.drawer.update()
            QApplication.processEvents()

        self.current_vertex = where
        self.movement(net)


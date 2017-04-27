import time
import networkx as nx
from Road import Road
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint

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
    def __init__(self, v, drawer):
        self.velocity = v
        self.current_vertex = 1
        self.finish_vertex = 2
        self.drawer = drawer

    def way(self, net):
        return (nx.dijkstra_path(net.matrix, self.current_vertex, self.finish_vertex))[1]

    def movement(self, net):
        print('Прибыл в',self.current_vertex)
        time.sleep(1)
        if self.current_vertex == self.finish_vertex:
            return

        where = self.way(net)
        road = net.mat_object[self.current_vertex][where]
        for i in range(len(road.points)):
            time.sleep(1/self.velocity)
            self.current_point = road.points[i]
            self.drawer.objpoint = Point(self.current_point[0], self.current_point[1])
            self.drawer.update()
            QApplication.processEvents()

        self.current_vertex = where
        self.movement(net)


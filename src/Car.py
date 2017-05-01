import time
import networkx as nx
from Tracker import Tracker
from Points import Point, Vertex
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint
inf = 10 ** 6

class Car:
    def __init__(self, v, drawer):
        self.velocity = v
        self.drawer = drawer

    def way(self, net):
        return (nx.dijkstra_path(net.matrix, self.current_vertex, self.finish_vertex))[1]

    def moveAtoB(self, net, start, finish):
        self.current_vertex = start.name
        self.finish_vertex = finish.name
        self.tracker = Tracker()
        self.drawer.carList.append(self.tracker)
        self.movement(net)
        self.drawer.carList.remove(self.tracker)
        start.setUnallocated()
        finish.setUnallocated()
        self.drawer.update()

    def movement(self, net):
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
            point = Point(self.current_point[0], self.current_point[1])
            self.tracker.setPos(point)
            self.drawer.update()
            QApplication.processEvents()

        self.current_vertex = where
        self.movement(net)


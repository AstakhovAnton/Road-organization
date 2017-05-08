import time
import networkx as nx
from Tracker import Tracker
from Points import Point, Vertex
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint
import math
inf = 10 ** 6

class Car:
    def __init__(self, v, drawer):
        self.velocity = v
        self.drawer = drawer
        self.current_velocity = 5

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
        if self.current_vertex == self.finish_vertex:
            return

        where = self.way(net)
        best_len = inf
        best_road = 0
        for road in net.matrix[self.current_vertex][where].keys():
            if net.matrix[self.current_vertex][where][road]['weight'] < best_len:
                best_len = net.matrix[self.current_vertex][where][road]['weight']
                best_road = road

        vmin = 5
        distance = len(net.matrix[self.current_vertex][where][best_road]['dots'])
        for i in range(distance):
            if distance < 200:
                accel = distance / 2
            else:
                accel = 100

            if i <= accel:
                self.current_velocity = math.sqrt(vmin ** 2 + i/accel * (self.velocity ** 2 - vmin ** 2))

            if distance <= i + accel - 1:
                self.current_velocity = math.sqrt(self.velocity ** 2 - (accel - distance + i + 1)/accel * (self.velocity ** 2 - vmin ** 2))


            time.sleep(1/self.current_velocity)
            if distance > i + 10:
                while net.matrix[self.current_vertex][where][best_road]['on_road'][i + 10] == 1:
                    time.sleep(1/inf)
            if i > 0:
                     net.matrix[self.current_vertex][where][best_road]['on_road'][i - 1] = 0
            net.matrix[self.current_vertex][where][best_road]['on_road'][i] = 1
            self.current_point = net.matrix[self.current_vertex][where][best_road]['dots'][i]
            point = Point(self.current_point[0], self.current_point[1])
            self.tracker.setPos(point)
            self.drawer.update()
            QApplication.processEvents()

        net.matrix[self.current_vertex][where][best_road]['on_road'][i] = 0
        self.current_vertex = where
        self.movement(net)


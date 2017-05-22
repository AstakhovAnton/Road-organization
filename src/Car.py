import time
import networkx as nx
from Tracker import Tracker
from Points import Point, Vertex
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint
import math
inf = 10 ** 6
waiting = 1000

class Car:
    def __init__(self, v, drawer):
        self.velocity = v
        self.drawer = drawer
        self.current_velocity = 5

    def way(self, net, whence):
        return (nx.dijkstra_path(net.matrix, whence, self.finish_vertex))[1]

    def moveAtoB(self, net, start, finish):
        self.current_vertex = start.name
        self.start_vertex = start.name
        self.finish_vertex = finish.name
        self.tracker = Tracker()
        self.drawer.carList.append(self.tracker)
        self.movement(net)
        self.drawer.carList.remove(self.tracker)
        start.setUnallocated()
        finish.setUnallocated()

    def movement(self, net):
        if self.current_vertex == self.finish_vertex: ## if arrives
            return

        if self.current_vertex == self.start_vertex: ## if starts, where
            self.where = self.way(net, self.start_vertex)
            best_len = inf
            self.best_road = 0
            for road in net.matrix[self.current_vertex][self.where].keys():
                if net.matrix[self.current_vertex][self.where][road]['weight'] < best_len:
                    best_len = net.matrix[self.current_vertex][self.where][road]['weight']
                    self.best_road = road

        vmin = 2
        future_best_road = 0
        future_where = self.where
        distance = len(net.matrix[self.current_vertex][self.where][self.best_road]['dots']) ## traffic
        for i in range(distance):

            if self.where != self.finish_vertex and distance == i + 9: ## where
                future_where = self.way(net, self.where)
                best_len = inf
                future_best_road = 0
                for road in net.matrix[self.where][future_where].keys():
                    if net.matrix[self.where][future_where][road]['weight'] < best_len:
                        best_len = net.matrix[self.where][future_where][road]['weight']
                        future_best_road = road

            if distance < 200: ## to determine velocity
                accel = distance / 2
            else:
                accel = 100

            if i <= accel:
                self.current_velocity = math.sqrt(vmin ** 2 + i/accel * (self.velocity ** 2 - vmin ** 2))

            if distance <= i + accel - 1:
                self.current_velocity = math.sqrt(self.velocity ** 2 - (accel - distance + i + 1)/accel * (self.velocity ** 2 - vmin ** 2))

            if i != 0:
                time.sleep(1/self.current_velocity)


            no_wait = 0 ## when may go
            if distance > i + 10:
                while net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i + 10] == 1:
                    time.sleep(1/waiting)
            else:
                while no_wait == 0:
                    no_wait = 1



                    for close in nx.neighbors(net.matrix, self.where): ##do not merge
                        for road in net.matrix[self.where][close].keys():
                            num = 0
                            for point in net.matrix[self.where][close][road]['on_road']:
                                if num > 10 - distance + 1 + i:
                                    break
                                num += 1
                                if point == 1:
                                    no_wait *= 0


                    if no_wait == 0:
                        time.sleep(1/waiting)

            #if i < 35 or i > 400:
            #    print(i, self.velocity)

            net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i] = 1 ## car on road
            if i > 0:
                     net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i - 1] = 0

            self.current_point = net.matrix[self.current_vertex][self.where][self.best_road]['dots'][i]
            point = Point(self.current_point[0], self.current_point[1])
            self.tracker.setPos(point)

        net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][distance - 1] = 0
        self.current_vertex = self.where
        self.where = future_where
        self.best_road = future_best_road
        self.movement(net)


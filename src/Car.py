import time
import networkx as nx
from Tracker import Tracker
from Points import Point, Vertex
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, Qt, QPoint
import math
inf = 10 ** 6
waiting = 300

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
        self.future_best_road = 0
        self.future_where = self.where
        distance = len(net.matrix[self.current_vertex][self.where][self.best_road]['dots']) ## traffic
        for i in range(distance):

            if self.where != self.finish_vertex and distance == i + 30: ## where
                self.future_where = self.way(net, self.where)
                best_len = inf
                self.future_best_road = 0
                for road in net.matrix[self.where][self.future_where].keys():
                    if net.matrix[self.where][self.future_where][road]['weight'] < best_len:
                        best_len = net.matrix[self.where][self.future_where][road]['weight']
                        self.future_best_road = road

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
                while net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i + 10] != 0:
                    time.sleep(1/waiting)
            else:
                while no_wait == 0 and self.where != self.finish_vertex:
                    no_wait = 1

                    for vertex_predecessors in net.matrix.predecessors(self.where):
                        for road in net.matrix[vertex_predecessors][self.where].keys():
                            if vertex_predecessors != self.current_vertex or road != self.best_road: ## vertex_predecessors
                                first_angle = net.matrix[self.where][self.future_where][self.future_best_road]['start_angle'] ## edge
                                second_angle = net.matrix[self.current_vertex][self.where][self.best_road]['finish_angle']    ## edge
                                other_angle = net.matrix[vertex_predecessors][self.where][road]['finish_angle']
                                len_road = len(net.matrix[vertex_predecessors][self.where][road]['on_road'])
                                if second_angle < first_angle and second_angle < other_angle and other_angle < first_angle\
                                        or second_angle < other_angle and second_angle > first_angle\
                                        or second_angle > first_angle and second_angle > other_angle and first_angle > other_angle:
                                        for j in range(len_road - 30, len_road):
                                            if net.matrix[vertex_predecessors][self.where][road]['on_road'][j] != 0:
                                                if net.matrix[vertex_predecessors][self.where][road]['on_road'][j].future_best_road == self.future_best_road:
                                                    no_wait *= 0


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

            net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i] = self ## car on road
            if i > 0:
                     net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][i - 1] = 0

            self.current_point = net.matrix[self.current_vertex][self.where][self.best_road]['dots'][i]
            point = Point(self.current_point[0], self.current_point[1])
            self.tracker.setPos(point)

        net.matrix[self.current_vertex][self.where][self.best_road]['on_road'][distance - 1] = 0
        self.current_vertex = self.where
        self.where = self.future_where
        self.best_road = self.future_best_road
        self.movement(net)


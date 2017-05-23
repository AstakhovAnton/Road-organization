import networkx as nx
from math import atan2, degrees
from threading import Thread
from time import sleep
#from Car import Car


class Network:
    def __init__(self):
        self.matrix = nx.MultiDiGraph()
        Thread(target=self.dynamic_roads).start()

    def dynamic_roads(self):
        while 1:
            sleep(1)

            our_edges = self.matrix.edges()
            various_our_edges = set()

            for edges in our_edges:
                various_our_edges.add(edges)

            #for i in various_our_edges:
            #    for j in self.matrix[i[0]][i[1]]:
            #        print(self.matrix[i[0]][i[1]][j]['weight'])
            #print('###############################################################')

            for edges in various_our_edges:
                self.update_weigth(edges)

            #for i in various_our_edges:
            #   for j in self.matrix[i[0]][i[1]]:
            #       print(self.matrix[i[0]][i[1]][j]['weight'])
            #print('###############################################################')

    def update_weigth(self, edge):
        for road in self.matrix[edge[0]][edge[1]]:
            length = len(self.matrix[edge[0]][edge[1]][road]['on_road'])
            numbers_cars = 0
            place_car_min = 0
            velocity_min = 1000
            for i in range(length):
                if self.matrix[edge[0]][edge[1]][road]['on_road'][i] != 0:
                    numbers_cars += 1
                    if self.matrix[edge[0]][edge[1]][road]['on_road'][i].velocity < velocity_min:
                        velocity_min = self.matrix[edge[0]][edge[1]][road]['on_road'][i].velocity
                        place_car_min = i
                if numbers_cars != 0:
                    self.matrix[edge[0]][edge[1]][road]['weight'] = self.matrix[edge[0]][edge[1]][road]['weight_const'] * (1 + 30 * numbers_cars / length)


    def add_node(self, name):
        self.matrix.add_node(name)

    def add_edge(self, name1, name2, w, list_points):
        length = len(list_points)

        array_angle_s = []
        for i in range(8, 30, 2):
            array_angle_s.append(degrees(atan2(-list_points[i + 2][1] + list_points[i][1],  list_points[i + 2][0] - list_points[i][0])))
        array_angle_s.sort()
        first_angle = 0
        len_s = len(array_angle_s)
        for i in range(2, len_s - 2):
            first_angle += array_angle_s[i]
        first_angle /= len_s - 4

        array_angle_f = []
        for i in range(2, 30, 2):
            array_angle_f.append(degrees(atan2(list_points[length - i][1] - list_points[length - i - 2][1],  -list_points[length - i][0] + list_points[length - i - 2][0])))
        array_angle_f.sort()
        second_angle = 0
        len_f = len(array_angle_f)
        for i in range(2, len_f - 2):
            second_angle += array_angle_f[i]
        second_angle /= len_f - 4

        #print(first_angle, second_angle)
        self.matrix.add_edge(name1, name2, weight=w, weight_const=w, dots=list_points, on_road=[0] * length, start_angle=first_angle, finish_angle=second_angle)

    def remove_node(self, name):
        self.matrix.remove_node(name)
    def remove_edge(self, name1, name2):
        self.matrix.remove_edge(name1, name2)


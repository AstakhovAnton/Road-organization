import networkx as nx
from math import atan2, degrees
#from Car import Car

class Network:
    def __init__(self):
        self.matrix = nx.MultiDiGraph()

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
        self.matrix.add_edge(name1, name2, weight=w, dots=list_points, on_road=[0] * length, start_angle=first_angle, finish_angle=second_angle)

    def remove_node(self, name):
        self.matrix.remove_node(name)
    def remove_edge(self, name1, name2):
        self.matrix.remove_edge(name1, name2)


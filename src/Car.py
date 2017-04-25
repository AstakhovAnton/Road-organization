import time
import networkx as nx
from Road import Road

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
            self.drawer.update()

        self.current_vertex = where
        self.movement(net)

if __name__ == '__main__':

    road = Road([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    print(road)
    car = Car(2)
    car.movement(road)
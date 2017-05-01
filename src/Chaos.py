from drawer import Drawer
from fractions import Fraction
import random, threading, time
from Car import Car

class Chaos :
    def __init__(self,drawer):
        self.drawer = drawer
        self.net = self.drawer.net
        self.enum = self.net.number_of_edges
        self.probabilities = {}
        counter = 1
        for name in self.net.nodes():
            d = self.net.degree(name)
            self.probabilities.update([[name,[counter,counter+d-1]]])
            counter += d
        self.beginChaos()

    def beginChaos(self):
        def behaviour(net,startVN,drawer):
            nodes = self.net.nodes().copy()
            nodes.remove(startVN)
            endVN = random.choice(self.net.nodes)
            velocity = random.randint(5,15)*10
            for vert in drawer.vertices :
                if vert.name == startVN:
                    startV = vert
                    break

            for vert in drawer.vertices :
                if vert.name == endVN:
                    endV = vert
                    break

            car = Car(velocity,drawer)
            car.moveAtoB(drawer.net,startV,endV)

        for i in range(60):
            a = random.randint(1, 2 * self.enum)
            for key in self.probabilities.keys():
                if self.probabilities[key][0] <= a and self.probabilities[key][1] >= a:
                    startVN = key
            threading.Thread(target=behaviour, args=(self.net,startVN,self.drawer))
            time.sleep(1)

'''
if __name__ == '__main__':
    mynet = Network()
    for i in range(1, 4):
        mynet.add_node(i)
    mynet.add_edge(1, 2, 3, ((1, 1), (2, 2), (3, 3), (4, 4)))
    mynet.add_edge(1, 2, 4, ((1, 1), (2, 2), (3, 3), (4, 4)))
    mynet.add_edge(1, 3, 1, ((1, 1), (2, 2), (3, 3), (4, 4)))
    mynet.add_edge(3, 2, 1, ((1, 1), (2, 2), (3, 3), (4, 4)))
'''
import random, threading, time
from Car import Car
from PyQt5.QtWidgets import QApplication

class Chaos :
    def __init__(self,drawer):
        self.drawer = drawer
        self.net = self.drawer.net
        self.enum = self.net.matrix.number_of_edges()
        self.probabilities = {}
        counter = 1
        for name in self.net.matrix.nodes():
            d = self.net.matrix.degree(name)
            self.probabilities.update([[name,[counter,counter+d-1]]])
            counter += d
        self.beginChaos()

    def beginChaos(self):

        def behaviour(net,startVN,drawer, i):
            time.sleep(i/10)
            nodes = self.net.matrix.nodes().copy()
            nodes.remove(startVN)
            endVN = random.choice(self.net.matrix.nodes())
            velocity = random.randint(5,15)*40
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

        for i in range(600):
            a = random.randint(1, 2 * self.enum)
            for key in self.probabilities.keys():
                if self.probabilities[key][0] <= a and self.probabilities[key][1] >= a:
                    startVN = key
            threading.Thread(target=behaviour, args=(self.net,startVN,self.drawer, i)).start()


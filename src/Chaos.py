import random, threading, time
from Car import Car

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
        #print(self.enum)
        #print(counter)
        #print(self.probabilities)
        self.beginChaos()

    def beginChaos(self):

        def behaviour(net,startVN,drawer, i):
            time.sleep(i/10)
            nodes = self.net.matrix.nodes().copy()
            nodes.remove(startVN)
            endVN = random.choice(self.net.matrix.nodes())
            velocity = random.randint(5,15)*30
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
            #print(str(i) + '-ый цикл:')
            a = random.randint(1, 2 * self.enum)
            #print(a)
            for key in self.probabilities.keys():
                if self.probabilities[key][0] <= a and self.probabilities[key][1] >= a:
                    startVN = key
            #print(startVN)
            threading.Thread(target=behaviour, args=(self.net,startVN,self.drawer, i)).start()


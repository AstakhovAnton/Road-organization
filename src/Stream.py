import threading, time
from Car import Car

class Stream:
    def __init__(self, drawer, startV, endV, probability):
        self.drawer = drawer
        self.net = self.drawer.net
        self.endV = endV
        self.startV = startV
        self.probability = probability

        self.beginStream()

    def beginStream(self):
        def behavior(startV, endV, drawer, i, probability):
            time.sleep(i/probability)
            velocity = 200
            #velocity = random.randint(5,15)*20

            car = Car(velocity,drawer)
            car.moveAtoB(drawer.net,startV,endV)

        for i in range(120):
            threading.Thread(target=behavior, args=(self.startV, self.endV, self.drawer, i, self.probability)).start()
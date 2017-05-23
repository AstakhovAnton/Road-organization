
class Tracker:
    i = 1
    def __init__(self, car):
        self.pos = None
        self.car = car
        self.name = 'car' + str(Tracker.i)
        Tracker.i = Tracker.i + 1
        self.car.drawer.signal.addCarItem.emit(self.name, self.car.velocity, self.car.finish_vertex)

    def setPos(self, point):
        self.pos = point
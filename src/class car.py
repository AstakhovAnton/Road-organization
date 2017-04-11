import time

class Road:
    def __init__(self, listx, listy):
        self.points = []
        for i in range(len(listx)):
            self.points.append((listx[i], listy[i]))

    def roadStart(self):
        return self.points[0]


class Car:
    def __init__(self, v):

         self.velocity = v

    def searchForTheBestWay(self, graph):
         pass

    def movement(self, road):
        self.road = road
        for i in range(len(road.points)):
            time.sleep(1/self.velocity)
            self.current_point = road.points[i]
            print(self.current_point)

if __name__ == '__main__':

    road = Road([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    car = Car(2)
    car.movement(road)
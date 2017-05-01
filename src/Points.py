from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon
from Matrix import Network

class Point:
    def __init__(self, abs, ord):
        self.abs = abs
        self.ord = ord

    def x(self):
        return(self.abs)

    def y(self):
        return(self.ord)

    def myQPoint(self):
        return QPoint(self.abs, self.ord)

    @staticmethod
    def dist(point1, point2):
        return ((point2.x() - point1.x()) ** 2 + (point2.y() - point1.y()) ** 2) ** 0.5

class Vertex(Point):
    def __init__(self, abs, ord, net, name):
        super().__init__(abs, ord)
        self.name = name
        self.isBeginning = False
        self.isEnd = False
        self.addition(net)

    def addition(self, net):
        net.add_node(self.name)

    def setBeginning(self):
        self.isBeginning = True

    def setEnd(self):
        self.isEnd = True

    def setUnallocated(self):
        self.isBeginning = False
        self.isEnd = False

    def setName(self, str):
        self.name = str

    def getName(self):
        return self.name
    def extract(self):
        return (self.x(),self.y())

    c = ord('A')
    i = c

    @staticmethod
    def newVertex(x, y, net):
        if Vertex.i <= Vertex.c + 51:
            k = ((Vertex.i - Vertex.c) % 2) + 1
            name = chr(Vertex.c + (Vertex.i - Vertex.c) // 2 ) + str(k)
            Vertex.i = Vertex.i + 1
        else:
            name = ''
        v = Vertex(x, y, net, name)
        return v


class Road:
    def __init__(self, beginningVertex, net):
        self.vertex1 = beginningVertex
        self.ready = False
        self.isPrintable = True
        self.points = []
        self.net = net

    def finish(self, endingVertex, points):
        if self.ready == False:
            self.vertex2 = endingVertex
            self.points = points
            self.ready = True
            self.net.add_edge(self.vertex1.name, self.vertex2.name, len(self.points), self.extract())

    def polygonize(self):
        if self.ready:
            qpoints = []
            for point in self.points:
                qpoints.append(point.myQPoint())
            return QPolygon(qpoints)

    def extract(self):
        if self.ready:
            points = []
            for point in self.points:
                points.append((point.x(), point.y()))
            return points
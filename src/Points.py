from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon, QPen

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

    def extract(self):
        return (self.x(), self.y())


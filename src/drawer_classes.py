from drawer import Drawer
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QBrush, QFont
from PyQt5.QtCore import QObject, Qt, QPoint, QRect, pyqtSignal

class Communicate(QObject):
    switch = pyqtSignal()

class Controller:
    def __init__(self, drawer):
        self.drawer = drawer
        self.i = 1
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)

    def setControllerSchema(self):
        self.schema = (Drawer.pressMethods[self.i], Drawer.moveMethods[self.i], Drawer.drawMethods[self.i])

    def setDrawerSchema(self, schema):
        self.drawer.customMousePressEvent = schema[0]
        self.drawer.customMouseMoveEvent = schema[1]
        self.drawer.drawAdditional = schema[2]

    def switchBehavior(self):
        self.i = (self.i + 1) % 2
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)


class Point:
    def __init__(self, abs, ord):
        self.abs = abs
        self.ord = ord

    def x(self):
        return(self.abs)

    def y(self):
        return(self.ord)

    def QPoint(self):
        return QPoint(self.abs, self.ord)

    @staticmethod
    def dist(point1, point2):
        return (((point2.x() - point1.x()) ** 2 + (point2.y() - point1.y()) ** 2) ** 0.5)

class Vertex(Point):
    def __init__(self, abs, ord, name):
        super().__init__(abs, ord)
        self.name = name

    def setName(self, str):
        self.name = str

    c = ord('A')
    i = c

    @staticmethod
    def newVertex(x, y):
        if Vertex.i <= Vertex.c + 51:
            k = ((Vertex.i - Vertex.c) % 2) + 1
            name = chr(Vertex.c + (Vertex.i - Vertex.c) // 2 ) + str(k)
            Vertex.i = Vertex.i + 1
        else:
            name = ''
        v = Vertex(x, y, name)
        return v


class Road:
    def __init__(self, beginningVertex):
        self.vertex1 = beginningVertex
        self.ready = False
        self.points = []

    def finish(self, endingVertex, points):
        if self.ready == False:
            self.vertex2 = endingVertex
            self.points = points
            self.ready = True

    def polygonize(self):
        if self.ready:
            qpoints = []
            for point in self.points:
                qpoints.append(point.QPoint())
            return QPolygon(qpoints)

    def extract(self):
        if self.ready:
            points = []
            for point in self.points:
                points.append((point.x(), point.y()))
            return points

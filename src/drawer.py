import sys
from drawer_classes import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
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

class Drawer(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = Controller(self)
        self.signal = Communicate()
        self.signal.switch.connect(self.controller.switchBehavior)
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):

        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Drawer')
        self.vertices = []
        self.roads = []
        self.pointList = []
        self.show()
        self.pos = None

    def mousePressEvent(self, event):
        self.customMousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.customMouseMoveEvent(self, event)

    def drawCurve(self, qp):
        pen = QPen(Qt.black, 3, Qt.DashLine)
        qp.setPen(pen)
        points = []
        for point in self.pointList:
           points.append(point.QPoint())
        polygon = QPolygon(points)
        qp.drawPolyline(polygon)

    def paintEvent(self, event):
        q1 = QPainter()
        q4 = QPainter()

        for road in self.roads:
            q1.begin(self)
            pen = QPen(Qt.black, 3, Qt.DashLine)
            q1.setPen(pen)
            if road.ready:
                q1.drawPolyline(road.polygonize())
        for vertex in self.vertices:
            q4.begin(self)
            brush = QBrush(Qt.SolidPattern)
            q4.setBrush(brush)
            q4.drawEllipse(vertex.QPoint(), 7, 7)
            q4.setFont(QFont('Decorative', 10))
            q4.drawText(vertex.x() + 7, vertex.y() + 7, 30, 20, 0, vertex.name)
        q1.end()
        q4.end()
        self.drawAdditional(self)

    def closestvertex(self, point):
        distlist = []
        for vertex in self.vertices:
            distlist.append(Point.dist(point, vertex))
        if distlist:
            index = distlist.index(min(distlist))
            return self.vertices[index]
        else:
            return None

    def mindistance(self, point):
        distlist = []
        for vertex in self.vertices:
            distlist.append(Point.dist(point, vertex))
        if distlist:
            return min(distlist)
        else:
            return None

    def moveAndDraw(self, event):
        point = Point(event.x(), event.y())
        distance_from_previous_point = Point.dist(point, self.basepoint)
        self.pos = event.pos()
        if distance_from_previous_point >= 1:
            self.pointList.append(point)
            self.basepoint = point
            self.update()

        if self.mindistance(point) <= 7 and len(self.pointList) >= 20:
            v = self.closestvertex(point)
            self.pointList.append(Point(v.x(), v.y()))
            self.finishTheRoad(v)

            #points = []
            #for point in self.pointList:
                #points.append(point.QPoint())
            #self.roads.append(QPolygon(points))
            #self.pointList.clear()
            #self.signal.switch.emit()
            #self.pos = None

    def finishTheRoad(self, v):
        points = self.pointList.copy()
        road = self.newroad
        road.finish(v, points)
        self.roads.append(road)
        self.update()
        self.pointList.clear()
        self.signal.switch.emit()
        self.pos = None

    def noChanges(self, event):
        QWidget.mouseMoveEvent(self, event)

    def waitForFinish(self, event):
        if event.button() == Qt.LeftButton:
            point = Point(event.x(), event.y())
            self.pointList.append(point)
            v = Vertex.newVertex(event.x(), event.y())
            self.vertices.append(v)
            self.update()
            self.finishTheRoad(v)

            #points = []
            #for point in self.pointList:
               # points.append(point.QPoint())
            #self.roads.append(QPolygon(points))
            #self.pointList.clear()
            #self.signal.switch.emit()
            #self.pos = None

    def makeVertexStartRoad(self, event):
        if event.button() == Qt.RightButton:
            self.vertices.append(Vertex.newVertex(event.x(), event.y()))
            self.update()
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 8:
            v = self.closestvertex(point)
            self.newroad = Road(v)
            self.basepoint = Point(v.x(), v.y())
            self.pointList.append(self.basepoint)
            self.signal.switch.emit()

    def mouseTracePainter(self):
        q1 = QPainter()
        q1.begin(self)
        self.drawCurve(q1)
        if self.pos:
            q2 = QPainter()
            q2.begin(self)
            pen = QPen(Qt.black, 3, Qt.DashLine)
            q2.setPen(pen)
            q2.drawLine(self.pos.x(), self.pos.y(), self.pointList[-1].x(), self.pointList[-1].y())
            q2.end()

    def nothingToAdd(self):
        return

    pressMethods = (waitForFinish, makeVertexStartRoad)
    moveMethods = (moveAndDraw, noChanges)
    drawMethods = (mouseTracePainter, nothingToAdd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Drawer(None)
    sys.exit(app.exec_())

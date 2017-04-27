import sys, time
#from drawer_classes import *
from Matrix import Network
from Car import Car
from Road import Road
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QBrush, QFont
from PyQt5.QtCore import QObject, Qt, QPoint, QRect, pyqtSignal

class Communicate(QObject):
    switch = pyqtSignal()
    #switch2 = pyqtSignal()

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
        if self.i == 0:
            self.i = 1
        elif self.i == 1:
            self.i = 0
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)

    def switchByButton(self):
        if self.i == 1:
            self.i = 2
        elif self.i == 2:
            self.i = 1
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
        self.isBeginning = False
        self.isEnd = False

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
    def newVertex(x, y):
        if Vertex.i <= Vertex.c + 51:
            k = ((Vertex.i - Vertex.c) % 2) + 1
            name = chr(Vertex.c + (Vertex.i - Vertex.c) // 2 ) + str(k)
            Vertex.i = Vertex.i + 1
        else:
            name = ''
        v = Vertex(x, y, name)
        return v


class Road1:
    def __init__(self, beginningVertex):
        self.vertex1 = beginningVertex
        self.ready = False
        self.isPrintable = True
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
        self.btn = QPushButton('Переключение режимов', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(self.controller.switchByButton)
        self.vertices = []
        self.roads = []
        self.pointList = []
        self.show()
        self.count = 0
        self.pos = None
        self.hasBegun = False
        self.net = Network()

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
            if road.isPrintable:
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

    def finishTheRoad(self, v):
        points1 = self.pointList.copy()
        road1 = self.newroad
        road1.finish(v, points1)
        self.roads.append(road1)
        begv = self.newroad.vertex1
        points2 = self.pointList.copy()
        points2.reverse()
        road2 = Road1(v)
        road2.isPrintable = False
        road2.finish(begv, points2)
        self.roads.append(road2)
        self.update()
        self.pointList.clear()
        self.signal.switch.emit()
        self.pos = None
        self.objpoint = None

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


    def makeVertexStartRoad(self, event):
        if event.button() == Qt.RightButton:
            self.vertices.append(Vertex.newVertex(event.x(), event.y()))
            self.update()
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 8:
            v = self.closestvertex(point)
            self.newroad = Road1(v)
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

    def allocate(self, event):
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 7:
            if self.hasBegun == False:
                v = self.closestvertex(point)
                v.setBeginning()
                self.hasBegun = True
            else:
                self.closestvertex(point).setEnd()
            self.update()
            self.count += 1
            if self.count == 2:
                for road in self.roads:
                    if road.vertex1.isBeginning and road.vertex2.isEnd:
                        allocroad = road
                        break
                self.move(allocroad)
                self.count = 0
                for vertex in self.vertices:
                    if vertex.isBeginning or vertex.isEnd:
                        vertex.setUnallocated()
                self.hasBegun = False
                self.update()

    def move(self, road):
        name1 = road.vertex1.getName()
        name2 = road.vertex2.getName()
        roadpoints = road.extract()
        l = len(roadpoints)

        self.net.add_node(name1)
        self.net.add_node(name2)
        self.net.add_edge(1, 2, l, roadpoints)
        car = Car(200, self)

        car.movement(self.net)
        self.objpoint = None


    def nothingToAdd(self):
        return

    def drawAllocated(self):
        q1 = QPainter()
        for vertex in self.vertices:
            if vertex.isBeginning:
                q1.begin(self)
                pen = QPen(Qt.blue, 3, Qt.DashLine)
                q1.setPen(pen)
                q1.drawEllipse(vertex.QPoint(), 10, 10)
            elif vertex.isEnd:
                q1.begin(self)
                pen = QPen(Qt.red, 3, Qt.DashLine)
                q1.setPen(pen)
                q1.drawEllipse(vertex.QPoint(), 10, 10)

        q2 = QPainter()
        if self.objpoint:
            q2.begin(self)
            brush = QBrush(Qt.SolidPattern)
            q2.setBrush(brush)
            q2.drawEllipse(self.objpoint.QPoint(), 5, 5)

    pressMethods = (waitForFinish, makeVertexStartRoad, allocate)
    moveMethods = (moveAndDraw, noChanges, noChanges)
    drawMethods = (mouseTracePainter, nothingToAdd, drawAllocated)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Drawer(None)
    sys.exit(app.exec_())

import sys, time, math, threading
from Matrix import Network
from Car import Car
from Tracker import Tracker
from Points import Point, Vertex, Road
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
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
        self.drawer.update()

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
        self.carList = []
        self.show()
        self.count = 0
        self.pos = None
        self.hasBegun = False
        self.net = Network()

    def loadFromFile(self, verticeslist, roadlists):
        self.vertices = []
        self.roads = []
        for vcortege in verticeslist:
            self.vertices.append(Vertex.newVertex(vcortege[0], vcortege[1], self.net))
        for rlist in roadlists:
            for vertex in self.vertices:
                if vertex.x() == rlist[0][0] and vertex.y() == rlist[0][1]:
                    begv = vertex
            road = Road(begv, self.net)
            for vertex in self.vertices:
                if vertex.x() == rlist[-1][0] and vertex.y() == rlist[-1][1]:
                    endv = vertex
            points = []
            for cortege in rlist:
                points.append(Point(cortege[0], cortege[1]))
            road.finish(endv, points)


    def mousePressEvent(self, event):
        self.customMousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.customMouseMoveEvent(self, event)

    def drawCurve(self, qp):
        pen = QPen(Qt.black, 3, Qt.DashLine)
        qp.setPen(pen)
        points = []
        for point in self.pointList:
           points.append(point.myQPoint())
        polygon = QPolygon(points)
        qp.drawPolyline(polygon)

    def paintEvent(self, event):
        q1 = QPainter()
        q2 = QPainter()
        for road in self.roads:
            if road.isPrintable:
                q1.begin(self)
                pen = QPen(Qt.black, 3, Qt.DashLine)
                q1.setPen(pen)
                if road.ready:
                    q1.drawPolyline(road.polygonize())
        for vertex in self.vertices:
            q2.begin(self)
            brush = QBrush(Qt.SolidPattern)
            q2.setBrush(brush)
            q2.drawEllipse(vertex.myQPoint(), 7, 7)
            q2.setFont(QFont('Decorative', 10))
            q2.drawText(vertex.x() + 7, vertex.y() + 7, 30, 20, 0, vertex.name)
        q3 = QPainter()
        for vertex in self.vertices:
            if vertex.isBeginning:
                q3.begin(self)
                pen = QPen(Qt.blue, 3, Qt.DashLine)
                q3.setPen(pen)
                q3.drawEllipse(vertex.myQPoint(), 11, 11)
            if vertex.isEnd:
                q3.begin(self)
                pen = QPen(Qt.red, 2, Qt.DashLine)
                q3.setPen(pen)
                q3.drawEllipse(vertex.myQPoint(), 10, 10)
        q4 = QPainter()
        for tracker in self.carList:
            if tracker.pos:
                q4.begin(self)
                brush = QBrush(Qt.SolidPattern)
                q4.setBrush(brush)
                q4.drawEllipse(tracker.pos.myQPoint(), 5, 5)
        q1.end()
        q2.end()
        q3.end()
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
            if distance_from_previous_point >= 2:
                cos = (point.x() - self.basepoint.x()) / distance_from_previous_point
                sin = (point.y() - self.basepoint.y()) / distance_from_previous_point
                point = Point(self.basepoint.x() + round(cos), self.basepoint.y() + round(sin))
                for i in range(1, math.ceil(distance_from_previous_point)):
                    self.pointList.append(point)
                    point = Point(self.basepoint.x() + round(cos*i), self.basepoint.y() + round(sin*i))
            self.pointList.append(point)
            self.basepoint = point
            self.update()

        if self.mindistance(point) <= 7 and len(self.pointList) >= 20:
            v = self.closestvertex(point)
            self.pointList.append(Point(v.x(), v.y()))
            self.finishTheRoad(v)

    def previous(self, point):
        i = self.pointList.index(point)
        if i != 0:
            return self.pointList[i - 1]
        else:
            return Point(-1, -1)

    def finishTheRoad(self, v):
        for point in self.pointList:
            d = Point.dist(self.previous(point), point)
            if d == 0.0:
                self.pointList.remove(point)
        points1 = self.pointList.copy()
        road1 = self.newroad
        road1.finish(v, points1)
        self.roads.append(road1)
        begv = self.newroad.vertex1
        points2 = self.pointList.copy()
        points2.reverse()
        road2 = Road(v, self.net)
        road2.isPrintable = False
        road2.finish(begv, points2)
        self.roads.append(road2)
        self.update()
        self.pointList.clear()
        self.signal.switch.emit()
        self.pos = None

    def noChanges(self, event):
        QWidget.mouseMoveEvent(self, event)

    def waitForFinish(self, event):
        if event.button() == Qt.LeftButton:
            point = Point(event.x(), event.y())
            if self.mindistance(point) > 15:
                self.pointList.append(point)
                v = Vertex.newVertex(event.x(), event.y(), self.net)
                self.vertices.append(v)
                self.update()
                self.finishTheRoad(v)


    def makeVertexStartRoad(self, event):
        if event.button() == Qt.RightButton:
            point = Point(event.x(), event.y())
            if not self.vertices or self.mindistance(point) > 50:
                self.vertices.append(Vertex.newVertex(event.x(), event.y(), self.net))
                self.update()
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 8:
            v = self.closestvertex(point)
            self.newroad = Road(v, self.net)
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
        self.borderPaint()

    def allocate(self, event):
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 8:
            if self.hasBegun == False:
                self.v1 = self.closestvertex(point)
                self.v1.setBeginning()
                self.hasBegun = True
            else:
                self.v2 = self.closestvertex(point)
                self.v2.setEnd()
            self.update()
            self.count += 1
            if self.count == 2:
                self.move(self.v1, self.v2)
                self.count = 0
                self.hasBegun = False
                self.update()

    def move(self, v1, v2):
        def behavior(v, drawer, v1, v2):
            car = Car(v, drawer)
            car.moveAtoB(drawer.net, v1, v2)
        threading.Thread(target = behavior, args = (150, self, v1, v2,)).start()

    def nothingToAdd(self):
        self.borderPaint()

    def borderPaint(self):
        q = QPainter()
        for vertex in self.vertices:
            q.begin(self)
            brush = QBrush(Qt.BDiagPattern)
            pen = QPen(Qt.black, 1, Qt.DashLine)
            q.setBrush(brush)
            q.setPen(pen)
            q.drawEllipse(vertex.myQPoint(), 50, 50)
        q.end()

    def noBorders(self):
        return

    pressMethods = (waitForFinish, makeVertexStartRoad, allocate)
    moveMethods = (moveAndDraw, noChanges, noChanges)
    drawMethods = (mouseTracePainter, nothingToAdd, noBorders)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Drawer(None)
    sys.exit(app.exec_())

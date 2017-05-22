import sys, time, math, threading
from Matrix import Network
from Car import Car
from Points import Point, Vertex
from Road import Road
from Chaos import Chaos
from Stream import Stream
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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
        #self.drawer.update()

    def switchBehaviorToValue(self, i):
        self.i = i
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)
        #self.drawer.update()

    def switchBehaviorToDrawing(self):
        self.i = 1
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)

    def switchBehaviorToMovement(self):
        self.i = 2
        self.setControllerSchema()
        self.setDrawerSchema(self.schema)

    def setOneSided(self):
        self.drawer.isOneSided = True

    def setTwoSided(self):
        self.drawer.isOneSided = False

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
        self.carList = []
        self.show()
        self.count = 0
        self.pos = None
        self.hasBegun = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
        self.net = Network()
        self.n = 2
        self.isOneSided = False

    def loadFromFile(self, verticeslist, roadlists):
        pass
        self.vertices = []
        self.roads = []
        for vcortege in verticeslist:
            self.vertices.append(Vertex.newVertex(vcortege[0], vcortege[1], self.net))
        i = 0
        for rlist in roadlists:
            for vertex in self.vertices:
                if vertex.x() == rlist[0][0] and vertex.y() == rlist[0][1]:
                    begv = vertex
                    break
            road = Road(begv, self.net)
            for vertex in self.vertices:
                if vertex.x() == rlist[-1][0] and vertex.y() == rlist[-1][1]:
                    endv = vertex
                    break
            points = []
            for cortege in rlist:
                points.append(Point(cortege[0], cortege[1]))
            road.finish(endv, points)
            if i % 2 == 1:
                road.isPrintable = False
            i += 1
            self.roads.append(road)
        #self.update()


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
            if road.ready:
                road.draw(self, q1)

        q3 = QPainter()

        q4 = QPainter()
        for tracker in self.carList:
            if tracker.pos:
                q4.begin(self)
                brush = QBrush(Qt.SolidPattern)
                q4.setBrush(brush)
                q4.drawEllipse(tracker.pos.myQPoint(), 5, 5)

        for vertex in self.vertices:
            q2.begin(self)
            brush = QBrush(Qt.white, Qt.SolidPattern)
            pen = QPen(Qt.black, 3, Qt.DashLine)
            q2.setBrush(brush)
            q2.setPen(pen)
            q2.drawEllipse(vertex.myQPoint(), 50, 50)
            q2.setFont(QFont('Decorative', 10))
            q2.drawText(vertex.x() + 20, vertex.y() + 20, 30, 20, 0, vertex.name)
        for vertex in self.vertices:
            if vertex.isBeginning:
                q3.begin(self)
                pen = QPen(Qt.blue, 2, Qt.DashLine)
                q3.setPen(pen)
                q3.drawEllipse(vertex.myQPoint(), 50 , 50)
            if vertex.isEnd:
                q3.begin(self)
                pen = QPen(Qt.red, 2, Qt.DashLine)
                q3.setPen(pen)
                q3.drawEllipse(vertex.myQPoint(), 50, 50)
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
        m = 1
        point = Point(event.x(), event.y())
        distance_from_previous_point = Point.dist(point, self.basepoint)
        self.pos = event.pos()
        if distance_from_previous_point >= m:
            if distance_from_previous_point >= 2*m:
                cos = (point.x() - self.basepoint.x()) / distance_from_previous_point
                sin = (point.y() - self.basepoint.y()) / distance_from_previous_point
                point = Point(self.basepoint.x() + round(cos), self.basepoint.y() + round(sin))
                for i in range(m, math.ceil(distance_from_previous_point), m):
                    self.pointList.append(point)
                    point = Point(self.basepoint.x() + round(cos*i), self.basepoint.y() + round(sin*i))
            self.pointList.append(point)
            self.basepoint = point

        if self.mindistance(point) <= 20 and len(self.pointList) >= 50:
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
        points = self.pointList.copy()
        road = self.newroad
        road.found(points, v)
        self.roads.append(road)
        self.pointList.clear()
        self.signal.switch.emit()
        self.pos = None


    def noChanges(self, event):
        QWidget.mouseMoveEvent(self, event)

    def waitForFinish(self, event):
        if event.button() == Qt.LeftButton:
            point = Point(event.x(), event.y())
            if self.mindistance(point) > 100:
                self.pointList.append(point)
                v = Vertex.newVertex(event.x(), event.y(), self.net)
                self.vertices.append(v)
                self.finishTheRoad(v)


    def makeVertexStartRoad(self, event):
        if event.button() == Qt.RightButton:
            point = Point(event.x(), event.y())
            if not self.vertices or self.mindistance(point) > 50:
                self.vertices.append(Vertex.newVertex(event.x(), event.y(), self.net))
                #self.update()
        point = Point(event.x(), event.y())
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 20:
            v = self.closestvertex(point)
            self.newroad = Road(v, self.net, self.n, self.isOneSided)
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
        if event.button() == Qt.LeftButton and self.vertices and self.mindistance(point) <= 20:
            if self.hasBegun == False:
                self.v1 = self.closestvertex(point)
                self.v1.setBeginning()
                self.hasBegun = True
            else:
                self.v2 = self.closestvertex(point)
                self.v2.setEnd()
            #self.update()
            self.count += 1
            if self.count == 2:
                self.move(self.v1, self.v2)
                self.count = 0
                self.hasBegun = False
                #self.update()

    def move(self, v1, v2):
        s = Stream(self, v1, v2, 10)

    def chaos(self):
        self.controller.switchBehaviorToValue(2)
        c = Chaos(self)

    def nothingToAdd(self):
        self.borderPaint()

    def borderPaint(self):
        q = QPainter()
        for vertex in self.vertices:
            q.begin(self)
            brush = QBrush(Qt.BDiagPattern)
            pen = QPen(Qt.black, 1, Qt.DashLine)
            if self.pos and Point.dist(Point(self.pos.x(), self.pos.y()), vertex) <= 100:
                q.setBrush(brush)
            q.setPen(pen)
            q.drawEllipse(vertex.myQPoint(), 100, 100)
            q.end()

    def noBorders(self):
        return

    pressMethods = (waitForFinish, makeVertexStartRoad, allocate)
    moveMethods = (moveAndDraw, noChanges, noChanges)
    drawMethods = (mouseTracePainter, nothingToAdd, noBorders)

class AuxWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Drawer')
        self.show()

        self.drawer = Drawer(self)

        self.btn1 = QPushButton('Переключение режимов', self)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.drawer.controller.switchByButton)
        self.btn2 = QPushButton('Хаос', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.clicked.connect(self.drawer.chaos)
        self.btn3 = QPushButton('Одностороннее/Двустороннее движение', self)
        self.btn3.resize(self.btn3.sizeHint())
        self.btn3.clicked.connect(self.drawer.controller.switchRoadBuildingSchema)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn3)
        hbox.addStretch(1)
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)

        vbox = QVBoxLayout()
        vbox.addWidget(self.drawer)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuxWidget(None)
    sys.exit(app.exec_())

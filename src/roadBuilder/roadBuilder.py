import sys, time
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QBrush, QFont
from PyQt5.QtCore import Qt, QPoint, QRect


class CurveDrawer(QWidget):
    distance_from_previous_point = 0
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Curve Drawer')
        self.listx = []
        self.listy = []
        self.roads = []
        self.vertices = []
        self.show()
        self.isFinished = True
        self.pos = None
        self.objposx = None
        self.objposy = None

    def mousePressEvent(self, e):

        if e.button() == Qt.RightButton and self.isFinished == True and not self.objposx and not self.objposy:
            self.vertices.append(QPoint(e.x(), e.y()))
            self.update()

        if e.button() == Qt.LeftButton and self.isFinished == True \
            and not self.objposx and not self.objposy \
            and self.vertices and self.mindistance(e.x(), e.y()) <= 8:
            self.x0 = self.closestvertex(e.x(), e.y()).x()
            self.y0 = self.closestvertex(e.x(), e.y()).y()
            #self.x0 = e.x()
            #self.y0 = e.y()
            self.listx.append(self.x0)
            self.listy.append(self.y0)
            self.isFinished = False

        elif e.button() == Qt.LeftButton and self.isFinished == False:
            self.listx.append(e.x())
            self.listy.append(e.y())
            self.vertices.append(QPoint(e.x(), e.y()))
            self.update()
            self.objposx = self.listx[0]
            self.objposy = self.listy[0]
            self.move()


    def mouseMoveEvent(self, event):
        if not self.isFinished:
            def dist(x0, y0, x1, y1):
                return round(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)

            distance_from_previous_point = dist(event.x(), event.y(), self.x0, self.y0)
            self.pos = event.pos()
            if distance_from_previous_point >= 1:
                x1 = event.x()
                y1 = event.y()
                self.listx.append(x1)
                self.listy.append(y1)
                self.x0 = x1
                self.y0 = y1
            self.update()

            if self.mindistance(event.x(), event.y()) <= 7 and len(self.listx) >= 10:
                self.listx.append(self.closestvertex(event.x(), event.y()).x())
                self.listy.append(self.closestvertex(event.x(), event.y()).y())
                self.objposx = self.listx[0]
                self.objposy = self.listy[0]
                self.move()

    def paintEvent(self, event):
        q1 = QPainter()
        q2 = QPainter()
        q3 = QPainter()
        q4 = QPainter()

        for road in self.roads:
            q1.begin(self)
            pen = QPen(Qt.black, 3, Qt.DashLine)
            q1.setPen(pen)
            q1.drawPolyline(road)
        for vertex in self.vertices:
            q4.begin(self)
            brush = QBrush(Qt.SolidPattern)
            q4.setBrush(brush)
            q4.drawEllipse(vertex, 7, 7)
            q4.setFont(QFont('Decorative', 10))
            names = []
            for i in range(ord('A'), ord('Z') + 1):
                names.append(chr(i))
            text = names[self.vertices.index(vertex)]
            q4.drawText(vertex.x() + 7, vertex.y() + 7, 20, 20, 0, text)

        if self.pos and not self.isFinished:
            q2.begin(self)
            self.drawCurve(q2)
            q1.drawLine(self.pos.x(), self.pos.y(), self.listx[-1], self.listy[-1])
        elif self.pos and self.isFinished:
            q2.begin(self)
            self.drawCurve(q2)
            q3.begin(self)
            brush = QBrush(Qt.SolidPattern)
            q3.setBrush(brush)
            x = self.objposx
            y = self.objposy
            if self.objposx and self.objposy:
                q3.drawEllipse(QPoint(x, y), 5, 5)
        q1.end()
        q2.end()
        q3.end()

    def drawCurve(self, qp):
        pen = QPen(Qt.black, 3, Qt.DashLine)
        qp.setPen(pen)
        points = []
        for i in range(len(self.listx)):
           points.append(QPoint(self.listx[i], self.listy[i]))
        polygon = QPolygon(points)
        qp.drawPolyline(polygon)

    def move(self):
        self.isFinished = True
        for i in range(len(self.listx) - 1):
            time.sleep(0.01)
            self.objposx = self.listx[i + 1]
            self.objposy = self.listy[i + 1]
            self.update()
            QApplication.processEvents()
        self.objposx = None
        self.objposy = None
        self.update()
        self.pos = None
        points = []
        for i in range(len(self.listx)):
           points.append(QPoint(self.listx[i], self.listy[i]))
        self.roads.append(QPolygon(points))
        #print(self.listx)
        #print(self.listy)
        self.listx.clear()
        self.listy.clear()

    def closestvertex(self, x, y):
        def dist(x0, y0, x1, y1):
            return round(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
        distlist = []
        for vertex in self.vertices:
            distlist.append(dist(x, y, vertex.x(), vertex.y()))
        if distlist:
            index = distlist.index(min(distlist))
            return self.vertices[index]
        else:
            return None


    def mindistance(self, x, y):
        def dist(x0, y0, x1, y1):
            return round(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
        distlist = []
        for vertex in self.vertices:
            distlist.append(dist(x, y, vertex.x(), vertex.y()))
        if distlist:
            return min(distlist)
        else:
            return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CurveDrawer(None)
    sys.exit(app.exec_())

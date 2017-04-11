import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

pointxlist = []
pointylist = []

class CurveDrawer(QWidget):
    distance_from_previous_point = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Curve Drawer')
        self.listx = []
        self.listy = []
        #self.xfin = 250
        #self.yfin = 250
        self.show()
        self.isFinished = True
        self.pos = None

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton and self.isFinished == True:
            self.x0 = e.x()
            self.y0 = e.y()
            self.listx.append(self.x0)
            self.listy.append(self.y0)
            self.isFinished = False

        elif e.button() == Qt.LeftButton and self.isFinished == False:
            self.listx.append(e.x())
            self.listy.append(e.y())
            self.isFinished = True
            #self.mouseMoveEvent = super().mouseMoveEvent
            print(self.listx)
            print(self.listy)
            self.listx.clear()
            self.listy.clear()

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
           # if dist(self.x0, self.y0, self.xfin, self.yfin) <= 8:
           #     self.listx.append(self.xfin)
           #     self.listy.append(self.yfin)
           #     self.isFinished = True
           #     self.mouseMoveEvent = super().mouseMoveEvent
            self.update()

    def paintEvent(self, event):
        q1 = QPainter()
        q2 = QPainter()
        if self.pos and not self.isFinished:
            q2.begin(self)
            self.drawCurve(q2)
            q1.drawLine(self.pos.x(), self.pos.y(), self.listx[-1], self.listy[-1])
        elif self.pos and self.isFinished:
            q1.end()
            q2.end()
            self.pos = None

    def drawCurve(self, qp):

        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(len(self.listx)-1):
            qp.drawLine(self.listx[i], self.listy[i], self.listx[i+1], self.listy[i+1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CurveDrawer()
    sys.exit(app.exec_())

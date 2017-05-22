from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon, QPen
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import functions

class Road:
    def __init__(self, beginningVertex, net, n, isOneSided):
        self.vertex1 = beginningVertex
        self.ready = False
        self.net = net
        self.borders = []
        self.trajectories = []
        self.n = n
        self.isOneSided = isOneSided

    def found(self, points, endingVertex):
        if self.ready == False:
            self.vertex2 = endingVertex
            borderlist = []
            trajlist = []
            if self.isOneSided:
                if self.n % 2 == 0:
                    pointsList = functions.multiplecurves(points, self.n, 10)
                    borderlist.append(LaneBorder(points))
                    for i in range(0, len(pointsList) - 2, 2):
                        if i % 4 == 0:
                            pointsList[i].insert(0, self.vertex1)
                            pointsList[i].insert(len(pointsList[i + 1]), self.vertex2)
                            pointsList[i + 1].insert(0, self.vertex1)
                            pointsList[i + 1].insert(len(pointsList[i + 1]), self.vertex2)
                            trajlist.append(Trajectory(pointsList[i], True))
                            trajlist.append(Trajectory(pointsList[i + 1], True))
                        else:
                            borderlist.append(LaneBorder(pointsList[i]))
                            borderlist.append(LaneBorder(pointsList[i + 1]))
                    borderlist.append(SideBorder(pointsList[-2]))
                    borderlist.append(SideBorder(pointsList[-1]))
                else:
                    pointsList = functions.multiplecurves(points, self.n, 10)
                    trajlist.append(Trajectory(points, True))
                    for i in range(0, len(pointsList) - 2, 2):
                        if i % 4 == 0:
                            borderlist.append(LaneBorder(pointsList[i]))
                            borderlist.append(LaneBorder(pointsList[i + 1]))
                        else:
                            pointsList[i].insert(0, self.vertex1)
                            pointsList[i].insert(len(pointsList[i + 1]), self.vertex2)
                            pointsList[i + 1].insert(0, self.vertex1)
                            pointsList[i + 1].insert(len(pointsList[i + 1]), self.vertex2)
                            trajlist.append(Trajectory(pointsList[i], True))
                            trajlist.append(Trajectory(pointsList[i + 1], True))
                    borderlist.append(SideBorder(pointsList[-2]))
                    borderlist.append(SideBorder(pointsList[-1]))
            else:
                borderlist.append(DoubleSolid(points))
                pointsList = functions.multiplecurves(points, 2*self.n, 10)
                #for sublist in pointsList:
                 #   sublist.insert(0, self.vertex1)
                 #   sublist.insert(len(sublist), self.vertex2)
                for i in range(0, len(pointsList) - 2, 2):
                    if i % 4 == 0:
                        pointsList[i].insert(0, self.vertex1)
                        pointsList[i].insert(len(pointsList[i]), self.vertex2)
                        pointsList[i+1].insert(0, self.vertex1)
                        pointsList[i+1].insert(len(pointsList[i+1]), self.vertex2)
                        trajlist.append(Trajectory(pointsList[i], True))
                        trajlist.append(Trajectory(pointsList[i + 1], False))
                    else:
                        borderlist.append(LaneBorder(pointsList[i]))
                        borderlist.append(LaneBorder(pointsList[i + 1]))
                borderlist.append(SideBorder(pointsList[-2]))
                borderlist.append(SideBorder(pointsList[-1]))
            length = len(pointsList[-1])
            self.finish(length, borderlist, trajlist)

    def finish(self, length, borderslist, trajlist):
        if self.ready == False:
            self.length = length
            self.borders = borderslist
            self.trajectories = trajlist
            for trajectory in self.trajectories:
                if trajectory.isStraight:
                    self.net.add_edge(self.vertex1.name, self.vertex2.name, self.length, trajectory.extract())
                else:
                    self.net.add_edge(self.vertex2.name, self.vertex1.name, self.length, trajectory.extract())
            self.ready = True

    def draw(self, drawer, painter):
        for border in self.borders:
            border.draw(drawer, painter)

class RoadElement:
    def __init__(self, points):
        self.points = points

class Border(RoadElement):
    def draw(self, drawer, painter):
        pass

    def polygonize(self, points):
        qpoints = []
        for point in points:
            qpoints.append(point.myQPoint())
        return QPolygon(qpoints)

class DoubleSolid(Border):
    def __init__(self, points):
        super().__init__(points)
        list = functions.multiplecurves(points, 1, 2)
        self.p1 = self.polygonize(list[0])
        self.p2 = self.polygonize(list[1])

    def draw(self, drawer, painter):
        painter.begin(drawer)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPolyline(self.p1)
        painter.drawPolyline(self.p2)
        painter.end()

class LaneBorder(Border):
    def __init__(self, points):
        super().__init__(points)

    def draw(self, drawer, painter):
        painter.begin(drawer)
        pen = QPen(Qt.black, 2, Qt.DashLine)
        painter.setPen(pen)
        painter.drawPolyline(self.polygonize(self.points))
        painter.end()

class SideBorder(Border):
    def __init__(self, points):
        super().__init__(points)

    def draw(self, drawer, painter):
        painter.begin(drawer)
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPolyline(self.polygonize(self.points))
        painter.end()

class Trajectory(RoadElement):
    def __init__(self, points, isStraight):
        super().__init__(points)
        self.isStraight = isStraight

    def extract(self):
        points = []
        if self.isStraight:
            for point in self.points:
                points.append((point.x(), point.y()))
        else:
            p = self.points.copy()
            p.reverse()
            for point in p:
                points.append((point.x(), point.y()))
        return points
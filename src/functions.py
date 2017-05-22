import sys
from Points import Point
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def center(p1, p2, p3):
    x12 = p1.x() - p2.x()
    x23 = p2.x() - p3.x()
    x31 = p3.x() - p1.x()
    y12 = p1.y() - p2.y()
    y23 = p2.y() - p3.y()
    y31 = p3.y() - p1.y()
    z1 = (p1.x()) ** 2 + (p1.y()) ** 2
    z2 = (p2.x()) ** 2 + (p2.y()) ** 2
    z3 = (p3.x()) ** 2 + (p3.y()) ** 2

    zx = y12*z3 + y23*z1 + y31*z2
    zy = x12*z3 + x23*z1 + x31*z2
    z = x12*y31 - y12*x31

    a = - zx/(2*z)
    b = zy/(2*z)
    return QPoint(a, b)

def onLine(p1, p2, p3):
    if (p2.x() - p1.x())*(p3.y() - p2.y()) == (p3.x() - p2.x())*(p2.y() - p1.y()):
        return True
    else:
        return False

def lower(p1, p2, p3):
    return (p3.x() - p1.x())*(p2.y() - p1.y()) > (p3.y() - p1.y())*(p2.x() - p1.x())

def sidecurve(points, l):
    points1 = []
    points2 = []
    n = 6
    for i in range(n, len(points) - n):
        if onLine(points[i - n], points[i], points[i + n]) == False:
            p = center(points[i - n], points[i], points[i + n])
            p1 = QPoint(round(points[i].x() + (p.x() - points[i].x())*l/Point.dist(points[i], p)), round(points[i].y() + (p.y() - points[i].y())*l/Point.dist(points[i], p)))
            p2 = QPoint(round(points[i].x() - (p.x() - points[i].x()) * l / Point.dist(points[i], p)),
                   round(points[i].y() - (p.y() - points[i].y()) * l / Point.dist(points[i], p)))
            if lower(points[i-n], points[i], p1):
                points1.append(p1)
                points2.append(p2)
            else:
                points1.append(p2)
                points2.append(p1)
        else:
            n1 = points[i].y() - points[i - n].y()
            n2 = points[i - n].x() - points[i].x()
            #print(n1, n2)
            mod = (n1 ** 2 + n2 ** 2) ** 0.5
            p1 = QPoint(round(points[i].x() - n1 * l / mod), round(points[i].y() - n2 * l / mod))
            p2 = QPoint(round(points[i].x() + n1 * l / mod), round(points[i].y() + n2 * l / mod))
            #print(p1, p2)
            #if lower(points[i - 2], points[i], points1[-1]) == lower(points[i - 2], points[i], p1):
            if lower(points[i - n], points[i], p1):
                points1.append(p1)
                points2.append(p2)
            else:
                points1.append(p2)
                points2.append(p1)
            #else:
             #       points1.append(p2)
             #       points2.append(p1)

    return [points1, points2]

def multiplecurves(points, n, l):
    list = []
    for i in range(1, n):
        s = sidecurve(points, i*l)
        list.append(s[0])
        list.append(s[1])
    return list

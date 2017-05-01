import sys
#from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QMessageBox
#from PyQt5.QtWidgets import (QWidget, QToolTip,
#                             QPushButton, QApplication, QHBoxLayout, QVBoxLayout)
#from PyQt5.QtGui import QFont, QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from drawer import Drawer

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.widget = Drawer(self)
        self.setCentralWidget(self.widget)

        col = QColor(255, 255, 255)

        mydocwidget = QDockWidget('colour', self)

        btn = QPushButton('colour', self)
        btn.resize(btn.sizeHint())


        btn.clicked.connect(self.showDialog)

        mydocwidget.setWidget(btn)

        self.addDockWidget(Qt.BottomDockWidgetArea, mydocwidget)

        self.widget.setStyleSheet("QWidget { background-color: %s }"
                                    % col.name())


        exitAction = QAction(QIcon('../resources/exit2.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        previousAction = QAction(QIcon('../resources/left.png'), 'previous', self)
        previousAction.setShortcut('F4')
        previousAction.setStatusTip('previous')
        previousAction.triggered.connect(self.close)

        nextAction = QAction(QIcon('../resources/right.png'), 'next', self)
        nextAction.setShortcut('F3')
        nextAction.setStatusTip('next')
        nextAction.triggered.connect(self.close)

        saveAction = QAction(QIcon('../resources/save.png'), 'Save', self)
        saveAction.setShortcut('F2')
        saveAction.setStatusTip('save current file')
        saveAction.triggered.connect(self.save)

        downloadAction = QAction(QIcon('../resources/globe.png'), 'Download', self)
        downloadAction.setShortcut('F5')
        downloadAction.setStatusTip('Download road network')
        downloadAction.triggered.connect(self.close)

        loadAction = QAction(QIcon('../resources/load.png'), 'load file', self)
        loadAction.setShortcut('F6')
        loadAction.setStatusTip('Download existing file')
        loadAction.triggered.connect(self.load)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        toolbar2 = self.addToolBar('Previous')
        toolbar2.addAction(previousAction)

        toolbar3 = self.addToolBar('next')
        toolbar3.addAction(nextAction)

        toolbar4 = self.addToolBar('Save')
        toolbar4.addAction(saveAction)

        toolbar5 = self.addToolBar('Download')
        toolbar5.addAction(downloadAction)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(400, 300, 450, 350)
        self.setWindowTitle('Main window')
        self.show()



    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def save(self):


        fd = open('Saves.txt', 'w')
        roads = self.widget.roads
        vertices = self.widget.vertices

        for vertex in vertices:
            cortege = vertex.extract()

            fd.write(str(cortege) + ' ')
        fd.write('\n')

        for road in roads:
            list = road.extract()

            for cortege in list:
                fd.write(str(cortege) + ' ')
            fd.write('\n')
        fd.close()
    def load(self):
        fd = open('Saves.txt', 'r')

        line = fd.readline()
        vertices = []
        roads = []
        list1 = line.split()
        list2 = []

        for element in list1:
            element = element.replace('(', '')
            element = element.replace(')', '')
            element = element.replace(',', '')
            element = element.replace(' ', '')
            list2.append(int(element))


        for i in range(len(list2)//2) :
            vertices.append((list2[2*i], list2[2*i+1]))

        road = []
        line = fd.readline()
        while line != '':
            line = fd.readline()
            list1 = line.split()
            list2 = []

            for element in list1:
                element = element.replace('(', '')
                element = element.replace(')', '')
                element = element.replace(',', '')
                element = element.replace(' ', '')
                list2.append(int(element))

            for i in range(len(list2) // 2):
                road.append((list2[2 * i], list2[2 * i + 1]))
            roads.append(road)

        fd.close()
        ##self.widget.loadFromFile(vertices, roads)

    def showDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.widget.setStyleSheet("QWidget { background-color: %s }"
                                    % col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
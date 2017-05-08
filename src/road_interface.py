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

        self.widget = MyWidget(self)
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




        exitAction = QAction( QIcon('../resources/exit2.png'),'Exit', self)
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
                                         "Save current file?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            result = self.save()
            if result == -1 :
                event.ignore()
    def save(self):

        fname = QFileDialog.getOpenFileName(self, 'save file', '/home')
        if fname[0]:
            fd = open(fname[0], 'w')
            roads = self.widget.drawer.roads
            vertices = self.widget.drawer.vertices

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
            return 0
        else:
            return -1
    def load(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            fd = open(fname[0], 'r')

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
            self.widget.drawer.loadFromFile(vertices, roads)

    def showDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.widget.setStyleSheet("QWidget { background-color: %s }"
                                    % col.name())

class MyWidget(QWidget) :


    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.drawer = Drawer(self)
        self.btn1 = QPushButton('Переключение режимов', self)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.drawer.controller.switchByButton)
        self.btn2 = QPushButton('Хаос', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.clicked.connect(self.drawer.chaos)

        #   self.btn3 = QPushButton('Одностороннее/Двустороннее движение', self)
        #  self.btn3.resize(self.btn3.sizeHint())
        # self.btn3.clicked.connect(self.drawer.controller.switchRoadBuildingSchema)

        oneSided = QAction('OneSided road', self)
        oneSided.triggered.connect(self.drawer.controller.setOneSided)

        twoSided = QAction('TwoSided road', self)
        twoSided.triggered.connect(self.drawer.controller.setTwoSided)

        self.listofactions = []
        self.listofactions.append(oneSided)
        self.listofactions.append(twoSided)

        btn3 = QComboBox(self)
        btn3.addItem('TwoSided road')
        btn3.addItem('OneSided road')

        btn3.activated[str].connect(self.chooseRoadSchema)

        hbox = QHBoxLayout()
        hbox.addWidget(btn3)
        hbox.addStretch(1)
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)


        vbox = QVBoxLayout()
        vbox.addWidget(self.drawer)

        vbox.addLayout(hbox)

        self.setLayout(vbox)
    def chooseRoadSchema(self, str):
        for action in self.listofactions :
            if action.text() == str :
                action.trigger()
                break


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
import sys


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from drawer import Drawer

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.CarList = CarListWidget(self)
        self.widget = MyWidget(self)
        self.setCentralWidget(self.widget)

        col = QColor(255, 255, 255)


        mydocwidget2 = QDockWidget('menu', self)
        mydocwidget2.setWidget(self.CarList)
        self.addDockWidget(Qt.RightDockWidgetArea, mydocwidget2)

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

        cleanAction = QAction(QIcon('../resources/cleaningicon.png'), 'Clean', self)
        cleanAction.setStatusTip('Clean screen')
        cleanAction.triggered.connect(self.clean)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(cleanAction)


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

        toolbar6 = self.addToolBar('Clean screen')
        toolbar6.addAction(cleanAction)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(300, 200, 650, 550)
        self.setWindowTitle('Main window')
        self.show()


    def clean(self):

        msg = QMessageBox.question(self, 'Question', "Are you sure to clean the screen?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.Yes:
            print('Yes')



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


            line = fd.readline()
            while line != '':
                road = []

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
                line = fd.readline()
            fd.close()
            self.widget.drawer.loadFromFile(vertices, roads)

    def showDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.widget.setStyleSheet("QWidget { background-color: %s }"
                                    % col.name())
            self.p.setColor(self.backgroundRole(), col)
            self.setPalette(self.p)

class MyWidget(QWidget) :


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.drawer = Drawer(self)

        drawAction = QAction('Draw schema', self)
        drawAction.triggered.connect(self.drawer.controller.switchBehaviorToDrawing)

        moveAction = QAction('Motion', self)
        moveAction.triggered.connect(self.drawer.controller.switchBehaviorToMovement)

        self.listofactions2 = []
        self.listofactions2.append(drawAction)
        self.listofactions2.append(moveAction)

        self.btn1 = QComboBox(self)
        self.btn1.addItem('Draw schema')
        self.btn1.addItem('Motion')
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.setFont(QFont('SansSerif', 10))

        self.btn1.activated[str].connect(self.chooseWorkingType)


        self.btn2 = QPushButton('Chaos', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.clicked.connect(self.drawer.chaos)


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
        btn3.resize(btn3.sizeHint())
        btn3.setFont(QFont('SansSerif', 10))
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

    def chooseWorkingType(self, str):
        for action in self.listofactions2 :
            if action.text() == str :
                action.trigger()
                break

class CarListWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.myList = QListWidget(self)


    def addItem(self, name, vel, finish):
        self.myList.addItems([name + '  ' + str(vel) + '  ' + finish])
    def setNewVelocity(self, int, name):
        for i in range(self.myList.count()):
            item = self.myList.item(i)
            list = item.text().split()
            if list[0] == name:
                item.setText(list[0] + '  ' + list[1] + '  ' + list[2] + '  ' + str(int))
                break
    def removeItem(self, name):
        for i in range(self.myList.count()):
            item = self.myList.item(i)
            list = item.text().split()
            if list[0] == name:
                self.myList.takeItem(i)
                break


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
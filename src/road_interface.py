import sys
#from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QMessageBox
#from PyQt5.QtWidgets import (QWidget, QToolTip,
#                             QPushButton, QApplication, QHBoxLayout, QVBoxLayout)
#from PyQt5.QtGui import QFont, QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from Slava import Slava

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.widget = Slava.CurveDrawer(self)
        print(self.widget.vertices)
        self.setCentralWidget(self.widget)

        col = QColor(0, 0, 0)

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

        saveAction = QAction(QIcon('../resources/save.png'), 'save', self)
        saveAction.setShortcut('F2')
        saveAction.setStatusTip('save current file')
        saveAction.triggered.connect(self.save)

        downloadAction = QAction(QIcon('../resources/globe.png'), 'Download', self)
        downloadAction.setShortcut('F5')
        downloadAction.setStatusTip('Download road network')
        downloadAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

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
        verticeslist = self.widget.vertices

        coordlist = []
        for vertex in verticeslist:
            coordlist.append((vertex.x(), vertex.y()))
        for cortege in coordlist:
            fd.write(str(cortege) + ' ')
        fd.close()


    def showDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.widget.setStyleSheet("QWidget { background-color: %s }"
                                    % col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
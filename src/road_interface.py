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

        exitAction = QAction(QIcon('exit2.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        previousAction = QAction(QIcon('mask.png'), 'previous', self)
        previousAction.setShortcut(' ')
        previousAction.setStatusTip('previous')
        previousAction.triggered.connect(self.close)

        saveAction = QAction(QIcon('tip.png'), 'save', self)
        saveAction.setStatusTip('save current file')
        saveAction.triggered.connect(self.save)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        toolbar2 = self.addToolBar('Previous')
        toolbar2.addAction(previousAction)

        toolbar3 = self.addToolBar('Save')
        toolbar3.addAction(saveAction)


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

        print(verticeslist)
        coordlist = []
        for vertex in verticeslist:
            coordlist.append((vertex.x(), vertex.y()))
        for cortege in coordlist:
            fd.write(str(cortege) + ' ')
        fd.close()


class MyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        button = QPushButton('button')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(button)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ##self.setGeometry(400, 300, 450, 350)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
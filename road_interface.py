import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QMessageBox
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QFont, QIcon


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        ##textEdit = QTextEdit()
        ##self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit2.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        #toolbar2 = self.addToolBar('Previous')

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(350, 300)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)

        vbox = QVBoxLayout()
        #vbox.addMenuBar(menubar)
        #vbox.add
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
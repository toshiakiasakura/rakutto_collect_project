# coding: UTF-8

import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt, QTimer
import PyQt5.QtWidgets



class Test(QWidget):

    def __init__(self):
        app = QApplication(sys.argv)
        self.index = 1

        super().__init__()
        self.init_ui()
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

        self.setGeometry(0,0,100,100)

        app.exec_()

    def init_ui(self):
        btn1 = QPushButton("Start",self)
        btn1.clicked.connect(self.Start)

        btn2 = QPushButton("End",self)
        btn2.move(0,30)
        btn2.clicked.connect(self.End)

    def Start(self):
        self.timer.start(1000)#一秒間隔で更新

    def End(self):
        self.timer.stop()

    def update(self):
        self.index += 1 
        print(self.index)


if __name__ == '__main__':
    Test()


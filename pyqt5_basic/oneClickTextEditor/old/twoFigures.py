# usr/bin/python3
# coding:utf-8


import sys
import os
import time 
import numpy as np


from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt, QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib import animation
plt.rcParams['font.family'] = 'IPAPGothic' 


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initFigure()

        # timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

        self.flag = True


    def initUI(self):
        # For FigureWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # make FigureLayout. This FigureLayout will be added by vbox.
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # delete margin 
        self.FigureLayout.setContentsMargins(0,0,0,0)

        btn1 = QtWidgets.QPushButton("Start",self)
        btn1.clicked.connect(self.buttonClicked)
        btn2 = QtWidgets.QPushButton("End",self)
        btn2.clicked.connect(self.buttonClicked2)


        ##### alinment  #####
        nx = 1000
        ny = 600

        btn1.move(nx*0.8,ny*0.9)
        btn2.move(nx*0.7,ny*0.9)
        self.setGeometry(0,0,nx*0.9,ny)
        self.FigureWidget.setGeometry(0,0,nx*0.9,ny*0.9)

    def initFigure(self):
        # make Figure
        self.Figure = plt.figure()
        # add Figure to FigureCanvas
        self.FigureCanvas = FigureCanvas(self.Figure)

        # add FigureCanvas to Layout
        self.FigureLayout.addWidget(self.FigureCanvas)

        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.scatter(1,1)

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        self.timer.start(1000) # ms
        
    def buttonClicked2(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        self.timer.stop() 


    def update(self):
        self.axis.clear()
        if self.flag:
            self.axis.scatter([2,3],[2,2])
            self.flag = False
        else:
            self.axis.scatter(1,1)
            self.axis.scatter(50,50,color="white")
            self.axis.text(1,1,"あいうえお")
            self.flag = True
        self.FigureCanvas.draw()



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())

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
            self.hiraganaTable()
            self.flag = True
        self.FigureCanvas.draw()

    def hiraganaTable(self):
        base1 = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめも"
        base2 = "やゆよ"
        base3 = "らりるれろ"
        base4 = "わん"
        base5 = "、。？！「」"
        base6 = ["゛","゜","空白","削除"] 


        x = 0
        y = 1
        fontSize = 14
        self.axis.scatter([0,0,11,11],[0,6,0,6],color="white")
        for i in range(7):
            for j in range(5):
                self.axis.text(x + i,y + 5-j,base1[j + i*5],fontsize=fontSize)
        for i ,j in enumerate([0,2,4]):
            self.axis.text(x + 7,y + 5-j,base2[i],fontsize=fontSize)
        for i in range(5):
            self.axis.text(x + 8,y + 5-i,base3[i],fontsize=fontSize)
        for i, j in enumerate([0,4]):
            self.axis.text(x + 9,y + 5-j,base4[i],fontsize=fontSize)
        for i in range(6):
            self.axis.text(x + 10,y+ 5-i,base5[i],fontsize=fontSize)
        for i,t in enumerate(base6):    
            self.axis.text(x + 3 + i , y + -0.5, t,fontsize=fontSize)

        self.axis.get_xaxis().set_visible(False)
        self.axis.get_yaxis().set_visible(False)
        self.axis.spines["right"].set_visible(False)
        self.axis.spines["left"].set_visible(False)
        self.axis.spines["top"].set_visible(False)
        self.axis.spines["bottom"].set_visible(False)
        

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())

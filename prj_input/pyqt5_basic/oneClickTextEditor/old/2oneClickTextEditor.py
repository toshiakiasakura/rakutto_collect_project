# usr/bin/python3
# coding:utf-8


import sys
import os
import time 
import numpy as np
import itertools

from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt, QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib import animation
plt.rcParams['font.family'] = 'IPAPGothic' 


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resText = "ここにテキストが表示されます"
        self.interval = 1000

        self.initUI()
        self.initFigure()

        self.resText = ""

        # timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.stopFlag = False

        # word setting 
        self.phase = 0
        self.dict1= ["あ","は","゛","゜","空白","削除" ]
        self.words1 = itertools.cycle(self.dict1)
        self.dict2= { "あ" : "あかさたな", "は": "はまやらわ"}



    def initUI(self):
        # For FigureWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # make FigureLayout. This FigureLayout will be added by vbox.
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # delete margin 
        self.FigureLayout.setContentsMargins(0,0,0,0)

        btn1 = QtWidgets.QPushButton("Click",self)
        btn1.clicked.connect(self.buttonClicked)
        btn2 = QtWidgets.QPushButton("Stop",self)
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
        self.setPositionHiragana()
        self.hiraganaTable()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        if self.stopFlag==True:
            self.timer.start(self.interval)
            self.stopFlag = False
            return(0)

        if self.phase == 0:
            self.timer.start(self.interval) # ms
            self.phase = 1 

        elif self.phase == 1 : 
            if self.word == "あ" or self.word == "は": 
                self.phase = 2 
                self.words2 = itertools.cycle(self.dict2[self.word])
            else:
                self.phase = 1 
                self.words1 = itertools.cycle(self.dict1)

                if self.word == "削除":
                    self.resText = self.resText[:-1]
                elif self.word == "空白":
                    self.resText += "　"
                else:
                    self.resText += self.word



        
    def buttonClicked2(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        self.timer.stop() 
        self.stopFlag = True


    def update(self):
        self.axis.clear()
        if self.phase == 1:
            self.word = self.words1.__next__()
            self.hiraganaTable()
            self.writeRed(self.word)

        elif self.phase == 2:
            self.word = self.words2.__next__()
            self.hiraganaTable()
            self.writeRed(self.word)

        self.FigureCanvas.draw()

    def setPositionHiragana(self):
        base1 = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめも"
        base2 = "やゆよ"
        base3 = "らりるれろ"
        base4 = "わん"
        base5 = "、。？！「」"
        base6 = ["゛","゜","空白","削除"] 

        self.x = 0
        self.y = 1.5
        x = self.x
        y = self.y

        self.pos= {}
        for i in range(7):
            for j in range(5):
                self.pos[base1[j + i*5] ] = [x+ i, y+5-j]

        for i ,j in enumerate([0,2,4]):
            self.pos[base2[i]] = [x+7, y+5-j]

        for i in range(5):
            self.pos[ base3[i]] = [x +8 , y+5-i]

        for i, j in enumerate([0,4]):
            self.pos[ base4[i] ] = [x+9, y + 5- j]

        for i in range(6):
            self.pos[ base5[i] ] = [x+ 10, y + 5-i]

        for i,t in enumerate(base6):    
            self.pos[ t] = [x+ 3 + i , y+ -0.5]

    def hiraganaTable(self):
        self.fontSize = 20
        self.axis.scatter([0,0,11,11],[0,6,0,6],color="white")
        for k,v in self.pos.items():
            self.axis.text(v[0],v[1],k, fontsize = self.fontSize)

        self.axis.text(self.x, self.y - 1.5, self.resText,fontsize=self.fontSize - 2)


        self.axis.get_xaxis().set_visible(False)
        self.axis.get_yaxis().set_visible(False)
        self.axis.spines["right"].set_visible(False)
        self.axis.spines["left"].set_visible(False)
        self.axis.spines["top"].set_visible(False)
        self.axis.spines["bottom"].set_visible(False)
        
    def writeRed(self,str_):
        v = self.pos[str_]
        self.axis.text(v[0],v[1],str_,color="red", fontsize = self.fontSize)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())

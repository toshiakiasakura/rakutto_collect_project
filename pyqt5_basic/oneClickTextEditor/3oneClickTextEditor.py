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

        # set parameters 
        self.interval = 1000
        self.fontSize = 48
        self.path2Save = "text.txt"
        self.maxNumText = 17
    
        # init objects
        self.resText = "ここにテキストが表示されます"

        self.initUI()
        self.initFigure()

        self.resText = ""

        # timer setting
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.stopFlag = False
        self.waitFlag = False 
        self.waitOne = False

        # word setting 
        self.phase = 0
        self.dict1= ["あ","は","゛","゜","削除" ]
        self.words1 = itertools.cycle(self.dict1)
        self.dict2= { "あ" : "あかさたな", "は": "はまやらわ、"}
        self.dict3= { "あ" : "あいうえお", 
                    "か":"かきくけこ",
                    "さ":"さしすせそ",
                    "た":"たちつてと",
                    "な":"なにぬねの",
                    "は":"はひふへほ",
                    "ま":"まみむめも",
                    "や":"やゆよ",
                    "ら":"らりるれろ",
                    "わ":"わをんー",
                    "、":"、。？！「」"
                    }



    def initUI(self):
        # For FigureWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # make FigureLayout. This FigureLayout will be added by vbox.
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # delete margin 
        self.FigureLayout.setContentsMargins(0,0,0,0)

        btn1 = QtWidgets.QPushButton("Click")
        btn1.clicked.connect(self.buttonClicked)
        btn2 = QtWidgets.QPushButton("Stop")
        btn2.clicked.connect(self.buttonClicked2)
        btn3 = QtWidgets.QPushButton("Reset")
        btn3.clicked.connect(self.buttonClicked3)

        def setSpinValue(value):
            self.interval = value

            if not self.stopFlag :
                self.timer.stop() 
                self.stopFlag = True
        spin1 = QtWidgets.QSpinBox()
        spin1.setRange(1,10000)
        spin1.setSingleStep(1)
        spin1.setValue(2000)
        spin1.valueChanged.connect(setSpinValue)
        spinLabel = QtWidgets.QLabel("")#"間隔(ms)")

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(spinLabel)
        self.hbox.addWidget(spin1)
        self.hbox.addWidget(btn3)
        self.hbox.addWidget(btn2)
        self.hbox.addWidget(btn1)


        ##### alinment  #####
        nx = 1400
        ny = 700

        #self.hbox(nx*0.5,ny*0.9)
        #btn1.move(nx*0.8,ny*0.9)
        #btn2.move(nx*0.7,ny*0.9)
        #btn3.move(nx*0.6,ny*0.9)
        #spin1.move(nx*0.5,ny*0.92)
        self.setGeometry(0,0,nx*0.9,ny)
        self.FigureWidget.setGeometry(0,0,nx*0.9,ny*0.97)

    def initFigure(self):
        # make Figure
        self.Figure = plt.figure()
        # add Figure to FigureCanvas
        self.FigureCanvas = FigureCanvas(self.Figure)

        # add FigureCanvas to Layout
        self.FigureLayout.addWidget(self.FigureCanvas)

        # for control panel 
        self.FigureLayout.addLayout(self.hbox)

        self.axis = self.Figure.add_subplot(1,1,1)
        self.setPositionHiragana()
        self.hiraganaTable()

    def buttonClicked(self):
        sender = self.sender()

        if self.stopFlag==True:
            self.timer.start(self.interval)
            self.stopFlag = False
            return(0)
            
        if self.waitOne:
            return(0)
        self.waitFlag = True

        # phase actions
        if self.phase == 0:
            self.timer.start(self.interval) # ms
            self.phase = 1 
            self.word = "あ"
            self.statusBar().showMessage("Phase 1")

        elif self.phase == 1 : 
            if self.word == "あ" or self.word == "は": 
                self.phase = 2 
                self.statusBar().showMessage("Phase 2")
                self.words2 = itertools.cycle(self.dict2[self.word])
                self.plotWord = self.word
            else:
                self.phase = 1 
                self.statusBar().showMessage("Phase 1")
                self.words1 = itertools.cycle(self.dict1)

                if self.word == "削除":
                    self.resText = self.resText[:-1]
                #elif self.word == "空白":
                #    self.resText += "　"
                else:
                    self.resText += self.word

        elif self.phase == 2: 
            self.phase = 3 
            self.statusBar().showMessage("Phase 3")
            self.words3 = itertools.cycle(self.dict3[self.word])
            self.plotWord = self.word

        elif self.phase == 3:
            self.phase = 1 
            self.statusBar().showMessage("Phase 1")
            self.resText += self.word
            self.words1 = itertools.cycle(self.dict1)

        # text display options
        if len(self.resText) > self.maxNumText:
            while len(self.resText) > self.maxNumText:

                with open(self.path2Save, "a") as f: 
                    f.write(self.resText[0]) 
                self.resText = self.resText[1:]

    def buttonClicked2(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        self.timer.stop() 
        self.stopFlag = True

    def buttonClicked3(self):
        sender = self.sender()
        self.statusBar().showMessage("button was clicked")

        self.resText = ""

    def update(self):
        self.axis.clear()
        if self.waitFlag:
            self.waitFlag = False
            self.waitOne = True

            self.hiraganaTable()
            self.writeRed("待機")

            if self.phase == 1:
                self.region1()
            elif self.phase == 2:
                self.region2(self.plotWord)
            elif self.phase == 3:
                self.region3(self.plotWord)
            self.FigureCanvas.draw()
            return(0)
        else:
            self.waitOne = False

        if self.phase == 1:
            self.word = self.words1.__next__()
            self.hiraganaTable()
            self.writeRed(self.word)
            self.region1()

        elif self.phase == 2:
            self.word = self.words2.__next__()
            self.hiraganaTable()
            self.writeRed(self.word)
            self.region2(self.plotWord)

        elif self.phase == 3:
            self.word = self.words3.__next__()
            self.hiraganaTable()
            self.writeRed(self.word)
            self.region3(self.plotWord)

        self.FigureCanvas.draw()

    def setPositionHiragana(self):
        base1 = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめも"
        base2 = "やゆよ"
        base3 = "らりるれろ"
        base4 = "わをんー"
        base5 = "、。？！「」"
        base6 = ["゛","゜","削除"] 

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

        for i, j in enumerate([0,1,2,3]):
            self.pos[ base4[i] ] = [x+9, y + 5- j]

        for i in range(6):
            self.pos[ base5[i] ] = [x+ 10, y + 5-i]

        for i,t in enumerate(base6):    
            self.pos[ t ] = [x+ 5 + i , y+ -0.5]

        self.pos["待機"] = [ x , y + 6.5]

    def hiraganaTable(self):
        self.axis.set_xlim([-1,11])
        self.axis.set_ylim([0,8])
        for k,v in self.pos.items():
            if k == "待機" :
                size = self.fontSize - 5
            else: 
                size = self.fontSize
            self.axis.text(v[0],v[1],k, fontsize = size)

        self.axis.text(self.x, self.y - 2, self.resText,fontsize=self.fontSize - 5)


        self.axis.get_xaxis().set_visible(False)
        self.axis.get_yaxis().set_visible(False)
        self.axis.spines["right"].set_visible(False)
        self.axis.spines["left"].set_visible(False)
        self.axis.spines["top"].set_visible(False)
        self.axis.spines["bottom"].set_visible(False)
        
    def writeRed(self,str_):
        v = self.pos[str_]
        if str_ == "待機" :
            size = self.fontSize - 5
        else: 
            size = self.fontSize
        self.axis.text(v[0],v[1],str_,color="red", fontsize = size)

    def region1(self):
        for w in ["あ","は","゛","゜"]:
            v = self.pos[w]
            dif = 0.05
            difP = 0.95
            x0 = v[0] - dif  
            y0 = v[1] - dif 
            xx = [ x0 , x0 , x0 + difP , x0 + difP, x0 ]
            yy = [ y0 , y0 + difP + 0.05 , y0 + difP + 0.05 , y0 , y0 ]
            self.axis.plot(xx,yy,color = "green")

        v = self.pos["削除"]
        x0 = v[0] - dif  
        y0 = v[1] - dif 
        addDif = 1.65 
        xx = [ x0 , x0 , x0 + dif + addDif , x0 + dif + addDif, x0 ]
        yy = [ y0 , y0 + difP , y0 + difP , y0 , y0 ]
        self.axis.plot(xx,yy,color = "green")

    def region2(self,str_):
        v = self.pos[str_]
        dif = 0.05
        difP = 0.95
        x0 = v[0] - dif
        y0 = v[1] - dif
        if str_ == "あ":
            addDif = 4.8
        else:
            addDif = 5.8
        xx = [ x0 , x0 , x0 + dif + addDif , x0 + dif + addDif, x0 ]
        yy = [ y0 , y0 + difP , y0 + difP , y0 , y0 ]
        self.axis.plot(xx,yy,color = "green")

    def region3(self,str_):
        v = self.pos[str_]
        dif = 0.05
        difP = 0.95
        x0 = v[0] - dif
        y0 = v[1] - dif + difP 
        if str_ == "、":
            addDif = 6
        else:
            addDif = 5

        xx = [ x0 , x0, x0 + difP, x0 + difP, x0 ]
        yy = [ y0, y0 -addDif, y0 - addDif , y0 , y0]
        self.axis.plot(xx,yy,color = "green")

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())

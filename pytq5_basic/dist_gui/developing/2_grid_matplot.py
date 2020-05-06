# usr/bin/python3
# coding:utf-8

import sys
import os 
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 


import glob
from PIL import Image
from scipy.stats import norm

class Application(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()
    
        self.initFigure()
        self.UpdateFigure()
        self.initSlidebar()

    # initialize UI 
    def initUI(self):
        # For FigureWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # make FigureLayout. This FigureLayout will be added by vbox.
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # delett margin 
        self.FigureLayout.setContentsMargins(0,0,0,0)

        self.FileList = QtWidgets.QListWidget(self)

        # make ButtonsLayout
        self.ButtonWidget = QtWidgets.QWidget(self)

        # alinment 
        self.setGeometry(0,0,900,600)
        self.FigureWidget.setGeometry(200,0,700,500) 
        self.ButtonWidget.setGeometry(200,500,700,100)
        self.FileList.setGeometry(0,0,200,600)

    def initFigure(self):
        # make Figure 
        self.Figure = plt.figure()
        # add Figure to FigureCanvas 
        self.FigureCanvas = FigureCanvas(self.Figure)
        # add FigureCanvas to Layout
        self.FigureLayout.addWidget(self.FigureCanvas)
        
        
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot([1,2],[2,3])
        self.show()

    def initSlidebar(self):
        self.inputLine = QtWidgets.QLineEdit()
        self.outputLine = QtWidgets.QLineEdit()
        self.outputLine.setReadOnly(True)

        UpdateButton= QtWidgets.QPushButton("Update")
        UpdateButton.clicked.connect(self.UpdateGraph)

        lineLayout = QtWidgets.QGridLayout()
        lineLayout.addWidget(QtWidgets.QLabel("par1"),0,0)
        lineLayout.addWidget(self.inputLine,0,1)
        lineLayout.addWidget(QtWidgets.QLabel("mean"),1,0)
        lineLayout.addWidget(self.outputLine,1,1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(UpdateButton)
        
        buttonsLayout = QtWidgets.QHBoxLayout(self.ButtonWidget)
        buttonsLayout.addLayout(lineLayout)
        buttonsLayout.addLayout(vbox)


    def UpdateFigure(self):
        # delete previous figure
        self.FigureLayout.takeAt(0)
    
        self.Figure = plt.figure()
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot([1,4],[4,1])
        self.show()

        self.FigureCanvas = FigureCanvas(self.Figure)
        self.FigureLayout.addWidget(self.FigureCanvas)

    def UpdateGraph(self):
        # delete previous figure
        self.FigureLayout.takeAt(0)
        # release memory not to be heavy 
        plt.clf()

        # get random numbers from normal distribution 
        self.Figure = plt.figure()
        a = norm().rvs(size=10)
        b = norm().rvs(size=10)

        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.scatter(a,b)
        self.show()

        self.FigureCanvas = FigureCanvas(self.Figure)
        self.FigureLayout.addWidget(self.FigureCanvas)


    #this function is for reference 
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())





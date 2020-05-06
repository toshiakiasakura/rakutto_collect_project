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
from scipy.stats import expon

def GetNDigit(v,n = 5):
    v = str(v) 
    if len(v.replace(".","")) < n + 1:
        return(v)
    else:
        ind = 0 
        s = ""
        for i in range(1000):
            if v[i] == "." :
                s += v[i]
                continue
            else:
                s += v[i]
                ind += 1
            if ind >= n:
                return(s)
            




class Application(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()
    
        self.initFigure()
        self.UpdateFigure()
        self.initSlidebar()
        
        # initialize File list
        self.set_FileList()
        # define event when a file is changed 
        self.FileList.itemSelectionChanged.connect(self.FileListChanged)

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
        self.SubWidget = QtWidgets.QWidget(self)

        # alinment 
        self.setGeometry(0,0,900,600)
        self.FigureWidget.setGeometry(200,0,500,500) 
        self.ButtonWidget.setGeometry(200,500,500,100)
        self.SubWidget.setGeometry(700,0,200,600)
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
        self.par1= QtWidgets.QLineEdit()
        self.par2= QtWidgets.QLineEdit()
        self.outputLine = QtWidgets.QLineEdit()
        self.outputLine.setReadOnly(True)

        UpdateButton= QtWidgets.QPushButton("Update")
        UpdateButton.clicked.connect(self.UpdateDist)
        #UpdateButton.clicked.connect(self.UpdateGraph)
        #UpdateButton.clicked.connect(self.GetResults)

        self.lineLayout = QtWidgets.QGridLayout()
        self.lineLayout.addWidget(QtWidgets.QLabel("tau"),0,0)
        self.lineLayout.addWidget(self.par1,0,1)
        self.lineLayout.addWidget(QtWidgets.QLabel("alpha"),1,0)
        self.lineLayout.addWidget(self.par2,1,1)
        self.lineLayout.addWidget(QtWidgets.QLabel("mean"),2,0)
        self.lineLayout.addWidget(self.outputLine,2,1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(UpdateButton)
        
        self.buttonsLayout = QtWidgets.QHBoxLayout(self.ButtonWidget)
        self.buttonsLayout.addLayout(self.lineLayout)
        self.buttonsLayout.addLayout(vbox)

        #### for subwidget results ##### 
        self.MeanDisplay = QtWidgets.QLineEdit()
        self.VarianceDisplay = QtWidgets.QLineEdit()
        self.MedianDisplay = QtWidgets.QLineEdit()
        self.MeanDisplay.setReadOnly(True)
        self.VarianceDisplay.setReadOnly(True)
        self.MedianDisplay.setReadOnly(True)


        SubLineLayout = QtWidgets.QGridLayout()
        SubLineLayout.addWidget(QtWidgets.QLabel("Mean"),0,0)
        SubLineLayout.addWidget(self.MeanDisplay,0,1)
        SubLineLayout.addWidget(QtWidgets.QLabel("Variance"),1,0)
        SubLineLayout.addWidget(self.VarianceDisplay,1,1)
        SubLineLayout.addWidget(QtWidgets.QLabel("Median"),2,0)
        SubLineLayout.addWidget(self.MedianDisplay,2,1)

        self.SubWidgetLayout = QtWidgets.QVBoxLayout(self.SubWidget)
        self.SubWidgetLayout.addLayout(SubLineLayout)



    def UpdateFigure(self):
        # delete previous figure
        self.FigureLayout.takeAt(0)
    
        self.Figure = plt.figure()
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot([1,4],[4,1])
        self.show()

        self.FigureCanvas = FigureCanvas(self.Figure)
        self.FigureLayout.addWidget(self.FigureCanvas)

    def UpdateDist(self):
        if self.FileName == "Exponential":
            self.UpdateExponential()

    def UpdateExponential(self):
        # delete previous figure
        self.FigureLayout.takeAt(0)
        # release memory not to be heavy,and make figure  
        plt.clf()
        self.Figure = plt.figure()
        
        ### for update figure ### 
        text = self.par1.text()
        try:
            tau = float(text)
        except:
            QtWidgets.QMessageBox.about(self,"Error","Error Message\nput a value to parameter")
            return(0)
        ex = expon(scale=tau)
        x = np.linspace(ex.ppf(0.05),ex.ppf(0.95),1000)
        y = ex.pdf(x)

        # show the graph 
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot(x,y)
        title = "Exponential distribution   " \
            +r"$f(x) = \frac{1}{\tau}e^{-\frac{x}{\tau}}$" 
        self.axis.set_title(title)
        self.show()

        self.FigureCanvas = FigureCanvas(self.Figure)
        self.FigureLayout.addWidget(self.FigureCanvas)


        ### for obtaining mean,variance, and median
        text = self.par1.text()
        try:
            tau = float(text)
        except:
            QtWidgets.QMessageBox.about(self,"Error","Error Message\nput a value to parameter")
            return(0)
        self.MeanDisplay.setText(GetNDigit( tau))
        self.VarianceDisplay.setText(GetNDigit(tau**2))
        self.MedianDisplay.setText(GetNDigit(tau*np.log(2)))


    def set_FileList(self):
        # add names to File list
        self.names = ["Exponential","Exponential_Slidebar","Possion","other"]
        
        for name in self.names:
            self.FileList.addItem(name)


    def FileListChanged(self):
        # get file name opening 
        self.FileName = self.FileList.selectedItems()[0].text()

        # delete parameter input widgets 
        if self.lineLayout is not None:
            while self.lineLayout.count():
                item = self.lineLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        if self.FileName == "Exponential":
            self.initExponential()
            self.UpdateExponential()

        if self.FileName == "Exponential_Slidebar":
            self.initExponential_Slidebar()

    def initExponential_Slidebar(self):
        return(0)

    def initExponential(self):
        self.par1= QtWidgets.QLineEdit()
        self.par2= QtWidgets.QLineEdit()

        self.par1.setText(str(1))

        self.lineLayout.addWidget(QtWidgets.QLabel("tau"),0,0)
        self.lineLayout.addWidget(self.par1,0,1)
        self.lineLayout.addWidget(QtWidgets.QLabel("alpha"),1,0)
        self.lineLayout.addWidget(self.par2,1,1)

        self.outputLine = QtWidgets.QLineEdit()
        self.outputLine.setReadOnly(True)
        self.lineLayout.addWidget(self.outputLine,2,0)



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





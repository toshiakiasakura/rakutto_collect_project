# usr/bin/python3
# coding:utf-8

import sys
import os 
import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
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
    
        # initialize File list
        self.SetFileList()
        self.initFigure()
        self.initControlWidget()
        self.initResultWidget()
        self.initInfoWidget()
        self.UpdateDist()
        
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
        

        # make FileList,Info,Control,and Result widgests 
        self.FileList      = QtWidgets.QListWidget(self)
        self.ControlWidget = QtWidgets.QWidget(self)
        self.ResultWidget  = QtWidgets.QWidget(self)

        self.InfoWidget    = QtWidgets.QWidget(self)
        self.InfoLayout = QtWidgets.QVBoxLayout(self.InfoWidget)
        self.InfoLayout.setContentsMargins(0,0,0,0)

        # alinment 
        nx = 1000
        ny = 650
        self.setGeometry(0,0,nx,ny)
        self.FileList.setGeometry(0,0,nx*0.2,ny)
        self.FigureWidget.setGeometry(nx*0.2,0,nx*0.5,ny*0.7) 
        self.InfoWidget.setGeometry(nx*0.7,0,nx*0.3,ny*0.7)
        self.ControlWidget.setGeometry(nx*0.2,ny*0.7,nx*0.6,ny*0.3)
        self.ResultWidget.setGeometry(nx*0.8,ny*0.7,nx*0.2,ny*0.3)

    def initFigure(self):
        # make Figure 
        self.Figure = plt.figure()
        # add Figure to FigureCanvas 
        self.FigureCanvas = FigureCanvas(self.Figure)
        # add FigureCanvas to Layout
        self.FigureLayout.addWidget(self.FigureCanvas)
        
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot(1,1)
        
    def initControlWidget(self):
        
        self.sld = QtWidgets.QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(30, 40, 100, 30)
        
        self.sld.setFocusPolicy(Qt.StrongFocus)
        self.sld.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.sld.setTickInterval(30)
        self.sld.setSingleStep(1)
        self.sld.setMinimum(1)
        self.sld.setMaximum(10)

        # minimum and maximum box
        self.minimumSpinBox = QtWidgets.QDoubleSpinBox()
        self.minimumSpinBox.setRange(-100000,100000)
        self.minimumSpinBox.setSingleStep(1)
        self.minimumSpinBox.setValue(1)
        self.maximumSpinBox = QtWidgets.QDoubleSpinBox()
        self.maximumSpinBox.setRange(-100000,100000)
        self.maximumSpinBox.setSingleStep(1)
        self.maximumSpinBox.setValue(100)

        # set Bin Box 
        self.binSpinBox  = QtWidgets.QSpinBox()
        self.binSpinBox.setRange(1,10000)
        self.binSpinBox.setSingleStep(1)
        self.binSpinBox.setValue(10)

        # Showing current value         
        self.CurrentValue= QtWidgets.QDoubleSpinBox()
        self.CurrentValue.setRange(-10000,10000)
        self.CurrentValue.setSingleStep(0.01)
        self.CurrentValue.setValue(1)

        ##### setting signals #####
        self.minimumSpinBox.valueChanged.connect(self.CalcCurrentValue)
        self.maximumSpinBox.valueChanged.connect(self.CalcCurrentValue)
        self.binSpinBox.valueChanged.connect(self.sld.setMaximum)

        self.sld.valueChanged.connect(self.CalcCurrentValue)
#        self.CurrentValue.valueChanged.connect()
        # for updating figure
        self.CurrentValue.valueChanged.connect(self.AddExponential)


        ###### set layout of control box #####
        self.LineLayout = QtWidgets.QGridLayout()
        self.LineLayout.addWidget(QtWidgets.QLabel("pars"),0,0)
        self.LineLayout.addWidget(QtWidgets.QLabel("Min"),0,1)
        self.LineLayout.addWidget(QtWidgets.QLabel("Max"),0,2)
        self.LineLayout.addWidget(QtWidgets.QLabel("Bin"),0,3)
        self.LineLayout.addWidget(QtWidgets.QLabel("Slider"),0,4)
        self.LineLayout.addWidget(QtWidgets.QLabel("Value"),0,5)

        self.LineLayout.addWidget(QtWidgets.QLabel("tau"),1,0)
        self.LineLayout.addWidget(self.minimumSpinBox,1,1)
        self.LineLayout.addWidget(self.maximumSpinBox,1,2)
        self.LineLayout.addWidget(self.binSpinBox,1,3)
        self.LineLayout.addWidget(self.sld,1,4)
        self.LineLayout.addWidget(self.CurrentValue,1,5)

        
        # creat Option widgets
        self.SelectType = QtWidgets.QComboBox()
        self.SelectType.addItem("Probability Density Function")
        self.SelectType.addItem("Cumulative Density Function")
        self.ClearButton = QtWidgets.QPushButton("Clear")

        self.OptionLayout = QtWidgets.QHBoxLayout()
        self.OptionLayout.addWidget(self.SelectType)
        self.OptionLayout.addStretch(1)
        self.OptionLayout.addWidget(self.ClearButton)
        
        # signals for Option widgets
        self.ClearButton.clicked.connect(self.UpdateDist)
        
        # set this Control in ControlWidget
        self.vbox = QtWidgets.QVBoxLayout(self.ControlWidget)
        self.vbox.addLayout(self.LineLayout)
        self.vbox.addLayout(self.OptionLayout)
        self.vbox.addStretch(1)

    #### for ControlWidget #####    
    def CalcCurrentValue(self):
        min_ = self.minimumSpinBox.value()
        max_ = self.maximumSpinBox.value()
        bin_ = self.binSpinBox.value()
        sld_v = self.sld.value()

        CurrentValue_ = np.linspace(min_,max_,bin_)[sld_v-1]
        self.CurrentValue.setValue(CurrentValue_)

    #### for ResultWidget##### 
    def initResultWidget(self):

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

        self.SubWidgetLayout = QtWidgets.QVBoxLayout(self.ResultWidget)
        self.SubWidgetLayout.addLayout(SubLineLayout)
        self.SubWidgetLayout.addStretch(1)

    def initInfoWidget(self):
        # make Figure 
        self.InfoFigure= plt.figure()
        # add Figure to FigureCanvas 
        self.InfoCanvas = FigureCanvas(self.InfoFigure)
        # add InfoCanvas to Layout
        self.InfoLayout.addWidget(self.InfoCanvas)

        self.AxisInfo = self.InfoFigure.add_subplot(1,1,1)
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{1}{\tau}e^{-\frac{x}{\tau}}$" 
        expressions["CDF"]  = r"$1 - e^{-\frac{x}{\tau}} $"
        expressions["Mean"] = r"$\tau$"
        expressions["Variance"] = r"$\tau^2 $"
        expressions["Median"] = r"$\tau ln(2) $"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(0.0,1- i*0.1,ch)
            self.AxisInfo.text(0.3,1- i*0.1,":")
            self.AxisInfo.text(0.4,1- i*0.1, expressions[ch],fontsize = 12)


        self.AxisInfo.get_xaxis().set_visible(False)
        self.AxisInfo.get_yaxis().set_visible(False)
        self.AxisInfo.spines["right"].set_visible(False)
        self.AxisInfo.spines["left"].set_visible(False)
        self.AxisInfo.spines["top"].set_visible(False)
        self.AxisInfo.spines["bottom"].set_visible(False)
        self.show()
        

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
        # release memory not to be heavy,and make figure  
        self.axis.clear() 
        # delete previous figure
        #self.FigureLayout.takeAt(0)
        
        #self.Figure = plt.figure()
        
        ### for update figure ### 
        tau = self.CurrentValue.value()
        ex = expon(scale=tau)
        x = np.linspace(ex.ppf(0.05),ex.ppf(0.95),1000)
        y = ex.pdf(x)

        # create the graph 
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.plot(x,y,color=cm(i_th/n_bin))
        title = "Exponential distribution   " 
        self.axis.set_title(title)
        self.FigureCanvas.draw()

        #self.FigureCanvas = FigureCanvas(self.Figure)
        #self.FigureLayout.addWidget(self.FigureCanvas)


        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( tau))
        self.VarianceDisplay.setText(GetNDigit(tau**2))
        self.MedianDisplay.setText(GetNDigit(tau*np.log(2)))

    def AddExponential(self):
        tau = self.CurrentValue.value()
        
        self.axis = self.Figure.add_subplot(1,1,1)
        ex = expon(scale=tau)
        x = np.linspace(ex.ppf(0.05),ex.ppf(0.95),1000)
        y = ex.pdf(x)

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y,color = cm(i_th/n_bin))
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( tau))
        self.VarianceDisplay.setText(GetNDigit(tau**2))
        self.MedianDisplay.setText(GetNDigit(tau*np.log(2)))

    def SetFileList(self):
        # add names to File list
        self.names = ["Exponential","Exponential_Slidebar","Possion","other"]
        
        for name in self.names:
            self.FileList.addItem(name)

        self.FileName = self.names[0]    


    def FileListChanged(self):
        # get file name opening 
        self.FileName = self.FileList.selectedItems()[0].text()

        if self.FileName == "Exponential":
            #self.initExponential()
            self.UpdateExponential()

        if self.FileName == "Exponential_Slidebar":
            #self.initExponential_Slidebar()
            dammy = 1

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





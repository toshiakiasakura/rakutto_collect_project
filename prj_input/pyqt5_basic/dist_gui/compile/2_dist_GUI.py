# usr/bin/python3
# coding:utf-8

import sys
import os 
import numpy as np
import matplotlib.pyplot as plt
import time 

from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 

import glob
from scipy.stats import norm
from scipy.stats import expon
from scipy.stats import gamma
from scipy.stats import beta
from scipy.stats import poisson

### plot setting
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.linewidth"] = 0.3

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
#        self.axis.plot(1,1)
        
    def initControlWidget(self):
        
        self.LineLayout = QtWidgets.QGridLayout()
        # creat Option widgets
        self.SelectType = QtWidgets.QComboBox(self)

        self.SetSelectType("continuous")
        self.SelectType.highlighted.connect(self.UpdateDist)

        self.initExpoControl()
        
        self.PauseButton = QtWidgets.QPushButton("Pause")
        self.PauseButton.setCheckable(True)
        self.OneUpdateButton= QtWidgets.QPushButton("Update")
        self.ClearButton = QtWidgets.QPushButton("Clear")

        self.OptionLayout = QtWidgets.QHBoxLayout()
        self.OptionLayout.addWidget(self.SelectType)
        self.OptionLayout.addStretch(1)
        self.OptionLayout.addWidget(self.PauseButton)
        self.OptionLayout.addWidget(self.OneUpdateButton)
        self.OptionLayout.addWidget(self.ClearButton)
        
        # signals for Option widgets
        self.OneUpdateFlag = 0
        def flag1() : self.OneUpdateFlag = 1
        def flag0() : self.OneUpdateFlag = 0
        self.OneUpdateButton.clicked.connect(flag1)
        self.OneUpdateButton.clicked.connect(self.AddDist)
        self.OneUpdateButton.clicked.connect(flag0)
        self.ClearButton.clicked.connect(self.UpdateDist)
        
        
        # set this Control in ControlWidget
        self.vbox = QtWidgets.QVBoxLayout(self.ControlWidget)
        self.vbox.addLayout(self.LineLayout)
        self.vbox.addLayout(self.OptionLayout)
        self.vbox.addStretch(1)

    def SetSelectType(self,mode):
        if self.SelectType != None:
            self.SelectType.clear()
        if mode == "continuous":
            self.SelectType.addItem("Probability Density Function")
            self.SelectType.addItem("Cumulative Density Function")
        if mode == "discrete":
            self.SelectType.addItem("Probability Mass Function")
            self.SelectType.addItem("Cumulative Density Function")

    def initControl(self):

        self.slds = []
        self.minimumSpinBoxs = []
        self.maximumSpinBoxs = []
        self.binSpinBoxs = []
        self.CurrentValues = []
        for i in range(self.npar):
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
            self.minimumSpinBox.setRange(self.MinSpinRange[i][0],self.MinSpinRange[i][1])
            self.minimumSpinBox.setSingleStep(1)
            self.minimumSpinBox.setValue(self.MinSpinInit[i])
            self.maximumSpinBox = QtWidgets.QDoubleSpinBox()
            self.maximumSpinBox.setRange(self.MaxSpinRange[i][0],self.MaxSpinRange[i][1])
            self.maximumSpinBox.setSingleStep(1)
            self.maximumSpinBox.setValue(self.MaxSpinInit[i])

            # set Bin Box 
            self.binSpinBox  = QtWidgets.QSpinBox()
            self.binSpinBox.setRange(1,10000)
            self.binSpinBox.setSingleStep(1)
            self.binSpinBox.setValue(10)

            # Showing current value         
            self.CurrentValue= QtWidgets.QDoubleSpinBox()
            self.CurrentValue.setRange(self.CurrentRange[i][0],self.CurrentRange[i][1])
            self.CurrentValue.setSingleStep(0.01)
            self.CurrentValue.setValue(self.CurrentInit[i])
            
            # add to 's 
            self.slds.append(self.sld)
            self.minimumSpinBoxs.append(self.minimumSpinBox)
            self.maximumSpinBoxs.append(self.maximumSpinBox)
            self.binSpinBoxs.append(self.binSpinBox)
            self.CurrentValues.append(self.CurrentValue)

        ##### setting signals #####
        def f0(): self.ParameterIndex = 0
        def f1(): self.ParameterIndex = 1
        def f2(): self.ParameterIndex = 2
        def f3(): self.ParameterIndex = 3
        for i in range(self.npar):
            if i ==0:
                self.minimumSpinBoxs[i].valueChanged.connect(f0)
                self.maximumSpinBoxs[i].valueChanged.connect(f0)
                self.binSpinBoxs[i].valueChanged.connect(f0)
                self.slds[i].valueChanged.connect(f0)
            if i == 1:
                self.minimumSpinBoxs[i].valueChanged.connect(f1)
                self.maximumSpinBoxs[i].valueChanged.connect(f1)
                self.binSpinBoxs[i].valueChanged.connect(f1)
                self.slds[i].valueChanged.connect(f1)
            if i == 2:
                self.minimumSpinBoxs[i].valueChanged.connect(f2)
                self.maximumSpinBoxs[i].valueChanged.connect(f2)
                self.binSpinBoxs[i].valueChanged.connect(f2)
                self.slds[i].valueChanged.connect(f2)
            if i == 3:
                self.minimumSpinBoxs[i].valueChanged.connect(f3)
                self.maximumSpinBoxs[i].valueChanged.connect(f3)
                self.binSpinBoxs[i].valueChanged.connect(f3)
                self.slds[i].valueChanged.connect(f3)

            self.minimumSpinBoxs[i].valueChanged.connect(self.CalcCurrentValue)
            self.maximumSpinBoxs[i].valueChanged.connect(self.CalcCurrentValue)
            self.binSpinBoxs[i].valueChanged.connect(self.slds[i].setMaximum)

            self.slds[i].valueChanged.connect(self.CalcCurrentValue)
            # for updating figure
            self.CurrentValues[i].valueChanged.connect(self.AddDist)

        ###### set layout of control box #####
        self.LineLayout.addWidget(QtWidgets.QLabel("pars"),0,0)
        self.LineLayout.addWidget(QtWidgets.QLabel("Min"),0,1)
        self.LineLayout.addWidget(QtWidgets.QLabel("Max"),0,2)
        self.LineLayout.addWidget(QtWidgets.QLabel("Bin"),0,3)
        self.LineLayout.addWidget(QtWidgets.QLabel("Slider"),0,4)
        self.LineLayout.addWidget(QtWidgets.QLabel("Value"),0,5)

        ParName = ["tau"]
        for i in range(self.npar):
            self.LineLayout.addWidget(QtWidgets.QLabel(self.ParName[i]),i+1,0)
            self.LineLayout.addWidget(self.minimumSpinBoxs[i],i+1,1)
            self.LineLayout.addWidget(self.maximumSpinBoxs[i],i+1,2)
            self.LineLayout.addWidget(self.binSpinBoxs[i],i+1,3)
            self.LineLayout.addWidget(self.slds[i],i+1,4)
            self.LineLayout.addWidget(self.CurrentValues[i],i+1,5)

    def initExpoControl(self):
        # for parameter index
        self.ParameterIndex = 0
        # for initialize Comobox
        self.SetSelectType("continuous")

        self.npar = 1

        self.MinSpinRange = [[-100000,10000]]
        self.MaxSpinRange =  self.MinSpinRange
        self.MinSpinInit = [1]
        self.MaxSpinInit = [3]
        self.CurrentRange = self.MinSpinRange
        self.CurrentInit = [1]
        self.ParName = ["tau"]

        self.initControl()


    def initNormControl(self):
        # for parameter index
        self.ParameterIndex = 0
        self.SetSelectType("continuous")

        self.npar = 2

        self.MinSpinRange = [[-100000,10000],[0,10000]]
        self.MaxSpinRange =  self.MinSpinRange
        self.MinSpinInit = [-5,1]
        self.MaxSpinInit = [5,5]
        self.CurrentRange = self.MinSpinRange
        self.CurrentInit = [0,1]
        self.ParName = ["mu","sigma"]

        self.initControl()

    def initGammaControl(self):
        # for parameter index
        self.ParameterIndex = 0
        self.SetSelectType("continuous")

        self.npar = 2

        self.MinSpinRange = [[0,10000],[0,10000]]
        self.MaxSpinRange =  self.MinSpinRange
        self.MinSpinInit = [1,1]
        self.MaxSpinInit = [5,5]
        self.CurrentRange = self.MinSpinRange
        self.CurrentInit = [1,1]
        self.ParName = ["shape(a)","rate(b)"]

        self.initControl()


    def initBetaControl(self):
        # for parameter index
        self.ParameterIndex = 0
        self.SetSelectType("continuous")

        self.npar = 2

        self.MinSpinRange = [[0,10000],[0,10000]]
        self.MaxSpinRange =  self.MinSpinRange
        self.MinSpinInit = [1,1]
        self.MaxSpinInit = [10,10]
        self.CurrentRange = self.MinSpinRange
        self.CurrentInit = [1,1]
        self.ParName = ["a","b"]

        self.initControl()

    def initPoissonControl(self):

        # for parameter index
        self.ParameterIndex = 0
        # for initialize Comobox
        self.SetSelectType("discrete")

        self.npar = 1

        self.MinSpinRange = [[0,10000]]
        self.MaxSpinRange =  self.MinSpinRange
        self.MinSpinInit = [1]
        self.MaxSpinInit = [10]
        self.CurrentRange = self.MinSpinRange
        self.CurrentInit = [1]
        self.ParName = ["lambda"]

        self.initControl()


    #### for ControlWidget #####    
    def CalcCurrentValue(self):
        ind = self.ParameterIndex
        min_ = self.minimumSpinBoxs[ind].value()
        max_ = self.maximumSpinBoxs[ind].value()
        bin_ = self.binSpinBoxs[ind].value()
        sld_v = self.slds[ind].value()

        CurrentValue_ = np.linspace(min_,max_,bin_)[sld_v-1]
        self.CurrentValues[ind].setValue(CurrentValue_)

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
        
        self.initExpoInfo()

        self.AxisInfo.get_xaxis().set_visible(False)
        self.AxisInfo.get_yaxis().set_visible(False)
        self.AxisInfo.spines["right"].set_visible(False)
        self.AxisInfo.spines["left"].set_visible(False)
        self.AxisInfo.spines["top"].set_visible(False)
        self.AxisInfo.spines["bottom"].set_visible(False)
        
    def initExpoInfo(self):
        self.AxisInfo.clear()
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{1}{\tau}e^{-\frac{x}{\tau}}$" 
        expressions["CDF"]  = r"$1 - e^{-\frac{x}{\tau}} $"
        expressions["Mean"] = r"$\tau$"
        expressions["Variance"] = r"$\tau^2 $"
        expressions["Median"] = r"$\tau ln(2) $"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(-0.1,1- i*0.1,ch)
            self.AxisInfo.text(0.2,1- i*0.1,":")
            self.AxisInfo.text(0.25,1- i*0.1, expressions[ch],fontsize = 12)

        self.InfoCanvas.draw()

    def initNormInfo(self):
        self.AxisInfo.clear()
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{1}{\sqrt{2\pi \sigma^2}}\exp(-\frac{1}{2}(\frac{x - \mu}{\sigma})^2)$" 
        expressions["CDF"]  = r"$ \frac{1}{\sqrt{2\pi \sigma^2}}\int_{-\infty}^x \exp(-\frac{1}{2}(\frac{x-\mu}{\sigma})^2)dx $"
        expressions["Mean"] = r"$\mu$"
        expressions["Variance"] = r"$\sigma^2 $"
        expressions["Median"] = r"$\mu $"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(-0.1,1- i*0.1,ch)
            self.AxisInfo.text(0.2,1- i*0.1,":")
            self.AxisInfo.text(0.25,1- i*0.1, expressions[ch],fontsize = 10)

        self.InfoCanvas.draw()

    def initGammaInfo(self):
        self.AxisInfo.clear()
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{b^a}{\Gamma(a)}x^{a-1}e^{-bx}$" 
        expressions["CDF"]  = r"$ \frac{b^a}{\Gamma(a)}\int_0^x x^{a-1}e^{-bx}dx$"
        expressions["Mean"] = r"$\frac{a}{b}$"
        expressions["Variance"] = r"$\frac{a}{b^2} $"
        expressions["Median"] = "not simple"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(-0.1,1- i*0.1,ch)
            self.AxisInfo.text(0.2,1- i*0.1,":")
            self.AxisInfo.text(0.25,1- i*0.1, expressions[ch],fontsize = 10)

        self.InfoCanvas.draw()

    def initBetaInfo(self):
        self.AxisInfo.clear()
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}x^{a-1}(1-x)^{b-1}$"
        expressions["CDF"]  = r"$\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\int_0^{\infty} x^{a-1}(1-x)^{b-1}dx $"
        expressions["Mean"] = r"$\frac{a}{a+b}$"
        expressions["Variance"] = r"$\frac{ab}{(a+b)^2(a+b+1) }$"
        expressions["Median"] = r"$\approx \frac{a - \frac{1}{3}}{a+b - \frac{2}{3}}$"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(-0.1,1- i*0.1,ch)
            self.AxisInfo.text(0.2,1- i*0.1,":")
            self.AxisInfo.text(0.25,1- i*0.1, expressions[ch],fontsize = 10)

        self.InfoCanvas.draw()

    def initPoissonInfo(self):
        self.AxisInfo.clear()
        characters = ["PDF","CDF","Mean","Variance","Median"]

        expressions ={} 
        expressions["PDF"]  = r"$\frac{\lambda^k e^{-\lambda}}{k!}$"
        expressions["CDF"]  = r"$e^{-\lambda}\sum_{i=0}^{\lfloor k \rfloor}\frac{\lambda^i}{i!}$"
        expressions["Mean"] = r"$\lambda$"
        expressions["Variance"] = r"$\lambda$"
        expressions["Median"] = r"$\approx \lfloor \lambda + 1/3 - 0.02/\lambda \rfloor$"
        for i, ch in enumerate(characters):
            self.AxisInfo.text(-0.1,1- i*0.1,ch)
            self.AxisInfo.text(0.2,1- i*0.1,":")
            self.AxisInfo.text(0.25,1- i*0.1, expressions[ch],fontsize = 10)

        self.InfoCanvas.draw()

    def UpdateDist(self):
        self.axis.cla()
        self.FigureCanvas.draw()
        self.AddDist()

            
    def AddDist(self):
        if self.PauseButton.isChecked() and self.OneUpdateFlag == 0 :
            return(0)
       
        if self.FileName == "Exponential":
            self.AddExponential()
        if self.FileName == "Normal":
            self.AddNormal()
        if self.FileName == "Gamma":
            self.AddGamma()
        if self.FileName == "Beta":
            self.AddBeta()
        if self.FileName == "Poisson":
            self.AddPoisson()
            
    def AddExponential(self):
        tau = self.CurrentValues[0].value()
        
        #self.axis = self.Figure.add_subplot(1,1,1)
        ex = expon(scale=tau)
        x = np.linspace(ex.ppf(0.05),ex.ppf(0.95),1000)
        if self.SelectType.currentText() == "Probability Density Function":
            y = ex.pdf(x)
        elif self.SelectType.currentText() == "Cumulative Density Function":
            y = ex.cdf(x)
        else:
            x = 1
            y = 1

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y ,color = cm(i_th/n_bin))
        self.axis.set_title("Exponential Distribution")
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( tau))
        self.VarianceDisplay.setText(GetNDigit(tau**2))
        self.MedianDisplay.setText(GetNDigit(tau*np.log(2)))

    def AddNormal(self):
        mu = self.CurrentValues[0].value()
        sigma = self.CurrentValues[1].value()
        
        nm= norm(loc = mu,scale = sigma)
        x = np.linspace(nm.ppf(0.05),nm.ppf(0.95),1000)
        if self.SelectType.currentText() == "Probability Density Function":
            y = nm.pdf(x)
        elif self.SelectType.currentText() == "Cumulative Density Function":
            y = nm.cdf(x)

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y,color = cm(i_th/n_bin))
        self.axis.set_title("Normal Distribution")
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( mu))
        self.VarianceDisplay.setText(GetNDigit(sigma**2))
        self.MedianDisplay.setText(GetNDigit(mu))

    def AddGamma(self):
        a = self.CurrentValues[0].value()
        b = self.CurrentValues[1].value()
        scale = 1/b
        
        gm= gamma(a = a,scale = scale)
        x = np.linspace(gm.ppf(0.05),gm.ppf(0.95),1000)
        if self.SelectType.currentText() == "Probability Density Function":
            y = gm.pdf(x)
        elif self.SelectType.currentText() == "Cumulative Density Function":
            y = gm.cdf(x)

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y,color = cm(i_th/n_bin))
        self.axis.set_title("Gamma Distribution")
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( a/b))
        self.VarianceDisplay.setText(GetNDigit(a/b**2))
        self.MedianDisplay.setText("not simple")

    def AddBeta(self):
        a = self.CurrentValues[0].value()
        b = self.CurrentValues[1].value()
        
        self.axis = self.Figure.add_subplot(1,1,1)
        be= beta(a = a,b= b)
        x = np.linspace(be.ppf(0.05),be.ppf(0.95),1000)
        if self.SelectType.currentText() == "Probability Density Function":
            y = be.pdf(x)
        elif self.SelectType.currentText() == "Cumulative Density Function":
            y = be.cdf(x)

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y,color = cm(i_th/n_bin))
        self.axis.set_title("Beta Distribution")
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( a/(a+b)))
        self.VarianceDisplay.setText(GetNDigit(a*b/(a+b)**2/(a+b+1)))
        self.MedianDisplay.setText(GetNDigit((a-1/3)/(a+b-2/3)))

    def AddPoisson(self):
        lam = self.CurrentValues[0].value()
        
        self.axis = self.Figure.add_subplot(1,1,1)
        pois = poisson(lam)
        x = [i for i in range(int(pois.ppf(0.05)),int(pois.ppf(0.95)+1))]
        if self.SelectType.currentText() == "Probability Mass Function":
            y = pois.pmf(x)
        elif self.SelectType.currentText() == "Cumulative Density Function":
            y = pois.cdf(x)

        # add to graph
        cm = plt.get_cmap("rainbow")
        n_bin = self.binSpinBox.value()
        i_th = self.sld.value()
        
        self.axis.plot(x,y,color = cm(i_th/n_bin))
        self.axis.set_title("Poisson Distribution")
        self.FigureCanvas.draw()

        ### for obtaining mean,variance, and median
        self.MeanDisplay.setText(GetNDigit( lam))
        self.VarianceDisplay.setText(GetNDigit(lam))
        if lam != 0:
            self.MedianDisplay.setText(GetNDigit(lam + 1/3 - 0.02/lam))
        else:
            self.MedianDisplay.setText("error")


    def SetFileList(self):
        # add names to File list
        self.names = ["Exponential","Normal","Poisson","Gamma","Beta"]
        
        for name in self.names:
            self.FileList.addItem(name)

        self.FileName = self.names[0]    


    def FileListChanged(self):
        # get file name opening 
        self.FileName = self.FileList.selectedItems()[0].text()

        if self.FileName == "Exponential":
            self.clearLayout(self.LineLayout)
            self.initExpoControl()        
            self.initExpoInfo()
            self.UpdateDist()

        if self.FileName == "Normal":
            self.clearLayout(self.LineLayout)
            self.initNormControl()
            self.initNormInfo()
            self.UpdateDist()

        if self.FileName == "Gamma":
            self.clearLayout(self.LineLayout)
            self.initGammaControl()
            self.initGammaInfo()
            self.UpdateDist()
            
        if self.FileName == "Beta":
            self.clearLayout(self.LineLayout)
            self.initBetaControl()
            self.initBetaInfo()
            self.UpdateDist()

        if self.FileName == "Poisson":
            self.clearLayout(self.LineLayout)
            self.initPoissonControl()
            self.initPoissonInfo()
            self.UpdateDist()

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





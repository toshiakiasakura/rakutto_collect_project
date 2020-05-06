#!usr/bin/python
# coding:utf-8


from PyQt5.QtWidgets import (QWidget, QSlider, 
    QLabel, QApplication)
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import numpy as np 

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(30, 40, 100, 30)
        
        self.sld.setFocusPolicy(Qt.StrongFocus)
        self.sld.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.sld.setTickInterval(30)
        self.sld.setSingleStep(1)
        self.sld.setMinimum(1)
        self.sld.setMaximum(10)

        # minimum and maximum box
        self.minimumSpinBox = QtWidgets.QSpinBox()
        self.minimumSpinBox.setRange(-100000,100000)
        self.minimumSpinBox.setSingleStep(1)
        self.minimumSpinBox.setValue(1)
        self.maximumSpinBox = QtWidgets.QSpinBox()
        self.maximumSpinBox.setRange(-100000,100000)
        self.maximumSpinBox.setSingleStep(1)
        self.maximumSpinBox.setValue(100)

        # set Bin Box 
        self.binSpinBox  = QtWidgets.QSpinBox()
        self.binSpinBox.setRange(1,10000)
        self.binSpinBox.setSingleStep(1)
        self.binSpinBox.setValue(10)

        # Showing current value         
        self.CurrentValue= QtWidgets.QSpinBox()
        self.CurrentValue.setRange(-10000,10000)
        self.CurrentValue.setSingleStep(1)

        # setting signals
        self.minimumSpinBox.valueChanged.connect(self.CalcCurrentValue)
        self.maximumSpinBox.valueChanged.connect(self.CalcCurrentValue)
        self.binSpinBox.valueChanged.connect(self.sld.setMaximum)

        self.sld.valueChanged.connect(self.CalcCurrentValue)
#        self.CurrentValue.valueChanged.connect()

        self.sld.valueChanged.connect(self.changeValue)

        # set layout of control box
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
        self.ResetButton = QtWidgets.QPushButton("Reset")

        self.OptionLayout = QtWidgets.QHBoxLayout()
        self.OptionLayout.addWidget(self.SelectType)
        self.OptionLayout.addStretch(1)
        self.OptionLayout.addWidget(self.ClearButton)
        self.OptionLayout.addWidget(self.ResetButton)
        
        self.test = QtWidgets.QPushButton("test")
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.LineLayout)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.OptionLayout)
        self.setLayout(self.vbox)
        

        self.setGeometry(300, 300, 500, 170)
        self.setWindowTitle('QSlider')
        self.show()
        
    def CalcCurrentValue(self):
        min_ = self.minimumSpinBox.value()
        max_ = self.maximumSpinBox.value()
        bin_ = self.binSpinBox.value()
        sld_v = self.sld.value()


        CurrentValue_ = np.linspace(min_,max_,bin_)[sld_v-1]
        self.CurrentValue.setValue(CurrentValue_)

        
    def changeValue(self, value):
        print(self.sld.value())

        if self.sld.value == 5:
            print(value)
        elif value > 0 and value <= 30:
            print(value , "kick")
        elif value > 30 and value < 80:
            print("koko")
        else:
            print("kokokokoko")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

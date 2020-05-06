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
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(QtWidgets.QLabel("pars"))
        self.hbox1.addWidget(QtWidgets.QLabel("Min"))
        self.hbox1.addWidget(QtWidgets.QLabel("Max"))
        self.hbox1.addWidget(QtWidgets.QLabel("Bin"))
        self.hbox1.addWidget(QtWidgets.QLabel("Slider"))
        self.hbox1.addWidget(QtWidgets.QLabel("Value"))

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addWidget(QtWidgets.QLabel("tau"))
        self.hbox2.addWidget(self.minimumSpinBox)
        self.hbox2.addWidget(self.maximumSpinBox)
        self.hbox2.addWidget(self.binSpinBox)
        self.hbox2.addWidget(self.sld)
        self.hbox2.addWidget(self.CurrentValue)
        
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addStretch(1)
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

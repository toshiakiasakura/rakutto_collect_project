# usr/bin/python3
# coding:utf-8


import sys
import os
import matplotlib.pyplot as plt
import time 


from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initFigure()


    def initUI(self):
        # For FigureWidget
        self.FigureWidget = QtWidgets.QWidget(self)
        # make FigureLayout. This FigureLayout will be added by vbox.
        self.FigureLayout = QtWidgets.QVBoxLayout(self.FigureWidget)
        # delete margin 
        self.FigureLayout.setContentsMargins(0,0,0,0)

        # alinment 
        nx = 1000
        ny = 600

        self.setGeometry(0,0,nx,ny)
        self.FigureWidget.setGeometry(0,0,nx,ny)

    def initFigure(self):
        # make Figure
        self.Figure = plt.figure()
        # add Figure to FigureCanvas
        self.FigureCanvas = FigureCanvas(self.Figure)

        # add FigureCanvas to Layout
        self.FigureLayout.addWidget(self.FigureCanvas)

        self.axis = self.Figure.add_subplot(1,1,1)
        self.axis.scatter(1,1)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    qapp = Application()
    qapp.show()
    sys.exit(app.exec_())

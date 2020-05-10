#!/usr/bin/python3
# coding:utf-8

import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

def factorial(n,m):

    return(n + m)
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.inputLine = QLineEdit()
        self.inputLine2 = QLineEdit()
        self.outputLine = QLineEdit()
        self.outputLine.setReadOnly(True)

        self.calcButton = QPushButton("&Calc")
        self.calcButton.clicked.connect(self.calc)

        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("num"), 0, 0)
        lineLayout.addWidget(self.inputLine, 0, 1)
        lineLayout.addWidget(QLabel("result"), 1, 0)
        lineLayout.addWidget(self.inputLine2, 1, 1)
        lineLayout.addWidget(QLabel("result"), 2, 0)
        lineLayout.addWidget(self.outputLine, 2, 1)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.calcButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Factorial")

    def calc(self):
        n = int(self.inputLine.text())
        m = int(self.inputLine2.text())
        r = factorial(n,m)
        self.outputLine.setText(str(r))





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


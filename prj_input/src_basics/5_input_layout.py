# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '4_input_layout.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
import types 


class Ui_scrollArea(object):


    def setupUi(self, scrollArea):
        scrollArea.setObjectName("scrollArea")
        mainWidth = 1000
        mainHeight = 600
        scrollArea.resize(mainWidth, mainHeight)
        scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollVerticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollVerticalLayout.setObjectName("scrollVerticalLayout")
        self.verticalLayoutScroll = QtWidgets.QVBoxLayout()
        self.verticalLayoutScroll.setObjectName("verticalLayoutScroll")

        self.setupGridLayoutTop()
        self.setupScrollMiddle()
        self.setupGridLayoutBottom()
        self.retranslateUi(scrollArea)

        QtCore.QMetaObject.connectSlotsByName(scrollArea)

    def setupGridLayoutTop(self):
        self.gridLayoutTop = QtWidgets.QGridLayout()
        self.gridLayoutTop.setObjectName("gridLayoutTop")

        self.comboRef1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboRef1.setObjectName("comboRef1")
        self.gridLayoutTop.addWidget(self.comboRef1, 0, 2, 1, 1)
        self.comboRef2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboRef2.setObjectName("comboRef2")
        self.gridLayoutTop.addWidget(self.comboRef2, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 0, 1, 1, 1)
        self.lineRow = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineRow.sizePolicy().hasHeightForWidth())
        self.lineRow.setSizePolicy(sizePolicy)
        self.lineRow.setMinimumSize(QtCore.QSize(50, 0))
        self.lineRow.setObjectName("lineRow")
        self.gridLayoutTop.addWidget(self.lineRow, 0, 0, 1, 1)
        self.lineRef1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef1.setObjectName("lineRef1")
        self.gridLayoutTop.addWidget(self.lineRef1, 0, 3, 1, 1)
        self.lineSearch = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineSearch.setObjectName("lineSearch")
        self.gridLayoutTop.addWidget(self.lineSearch, 0, 5, 1, 1)
        self.lineRef2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef2.setObjectName("lineRef2")
        self.gridLayoutTop.addWidget(self.lineRef2, 1, 3, 1, 1)
        self.comboSearch = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboSearch.setObjectName("comboSearch")
        self.gridLayoutTop.addWidget(self.comboSearch, 0, 4, 1, 1)
        self.pushNewRow = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushNewRow.sizePolicy().hasHeightForWidth())
        self.pushNewRow.setSizePolicy(sizePolicy)
        self.pushNewRow.setObjectName("pushNewRow")
        self.gridLayoutTop.addWidget(self.pushNewRow, 1, 0, 1, 1)
        self.pushSearch = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushSearch.setObjectName("pushSearch")
        self.gridLayoutTop.addWidget(self.pushSearch, 1, 4, 1, 2)

        self.verticalLayoutScroll.addLayout(self.gridLayoutTop)

    def setupScrollMiddle(self):
        self.scrollMiddle = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.scrollMiddle.setWidgetResizable(True)
        self.scrollMiddle.setObjectName("scrollMiddle")
        self.scrollMiddle.setMinimumSize(QtCore.QSize(500,300)) 
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontals = []
        self.labels = []
        self.comboBoxes = []
        self.lines = []
        self.horizontalSpacers = []

        for i in range(30):
            self.horizontalLayoutMacro = QtWidgets.QHBoxLayout()
            self.horizontalLayoutMacro.setObjectName("horizontalLayoutMacro")

            self.labelMacro = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            self.labelMacro.setObjectName("labelMacro")
            self.labelMacro.setText("fun fun fun")
            self.horizontalLayoutMacro.addWidget(self.labelMacro)

            # comboBox setting.
            self.comboBoxMacro = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
            self.comboBoxMacro.setObjectName("comboBoxMacro")
            self.comboBoxMacro.setMinimumSize(QtCore.QSize(150,0)) 
            self.comboBoxMacro.addItems( ["a","b","c"] ) 
            # initial color 
            pal = self.comboBoxMacro.palette()
            pal.setColor(QtGui.QPalette.Button, QtGui.QColor(255,255,255) )
            self.comboBoxMacro.setPalette(pal)
            def changeBack(self,s):
                ''' if compare with originla data and find difference, 
                change color '''
                pal = self.palette()
                pal.setColor(QtGui.QPalette.Button, QtGui.QColor(255,255,0) )
                self.setPalette(pal)
            self.comboBoxMacro.changeBack = types.MethodType(changeBack,self.comboBoxMacro)
            self.horizontalLayoutMacro.addWidget(self.comboBoxMacro)

            # lineEdit setting. 
            self.lineMacro = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
            self.lineMacro.setObjectName("lineMacro")
            self.lineRow.setMinimumSize(QtCore.QSize(150,0)) 
            self.horizontalLayoutMacro.addWidget(self.lineMacro)

            horizontalSpacerMacro = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # set object. 
            self.horizontalLayoutMacro.addItem(horizontalSpacerMacro)
            # add each objects. 
            self.horizontals.append(self.horizontalLayoutMacro)
            self.verticalLayout.addLayout(self.horizontalLayoutMacro)
            self.labels.append(self.labelMacro)
            self.comboBoxes.append(self.comboBoxMacro)
            self.lines.append(self.labelMacro)
            self.horizontalSpacers.append(self.horizontalLayoutMacro)

        self.scrollMiddle.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutScroll.addWidget(self.scrollMiddle)

    def setupGridLayoutBottom(self):
        self.gridLayoutBottom = QtWidgets.QGridLayout()
        self.gridLayoutBottom.setObjectName("gridLayoutBottom")
        self.lineSh2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSh2.sizePolicy().hasHeightForWidth())
        self.lineSh2.setSizePolicy(sizePolicy)
        self.lineSh2.setObjectName("lineSh2")
        self.gridLayoutBottom.addWidget(self.lineSh2, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayoutBottom.addItem(spacerItem2, 0, 2, 1, 1)
        self.pushButtonWrite = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonWrite.sizePolicy().hasHeightForWidth())
        self.pushButtonWrite.setSizePolicy(sizePolicy)
        self.pushButtonWrite.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButtonWrite.setObjectName("pushButtonWrite")
        self.gridLayoutBottom.addWidget(self.pushButtonWrite, 1, 3, 1, 1)
        self.lineSh1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSh1.sizePolicy().hasHeightForWidth())
        self.lineSh1.setSizePolicy(sizePolicy)
        self.lineSh1.setMinimumSize(QtCore.QSize(100, 0))
        self.lineSh1.setObjectName("lineSh1")
        self.gridLayoutBottom.addWidget(self.lineSh1, 0, 1, 1, 1)
        self.labelSh1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSh1.sizePolicy().hasHeightForWidth())
        self.labelSh1.setSizePolicy(sizePolicy)
        self.labelSh1.setObjectName("labelSh1")
        self.gridLayoutBottom.addWidget(self.labelSh1, 0, 0, 1, 1)
        self.labelSh2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSh2.sizePolicy().hasHeightForWidth())
        self.labelSh2.setSizePolicy(sizePolicy)
        self.labelSh2.setObjectName("labelSh2")
        self.gridLayoutBottom.addWidget(self.labelSh2, 1, 0, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayoutBottom.addWidget(self.pushButtonCancel, 1, 4, 1, 1)
        self.pushQuit = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushQuit.sizePolicy().hasHeightForWidth())
        self.pushQuit.setSizePolicy(sizePolicy)
        self.pushQuit.setMinimumSize(QtCore.QSize(100, 0))
        self.pushQuit.setObjectName("pushQuit")
        self.gridLayoutBottom.addWidget(self.pushQuit, 1, 5, 1, 1)
        self.verticalLayoutScroll.addLayout(self.gridLayoutBottom)
        self.scrollVerticalLayout.addLayout(self.verticalLayoutScroll)
        scrollArea.setWidget(self.scrollAreaWidgetContents)

    def retranslateUi(self, scrollArea):
        _translate = QtCore.QCoreApplication.translate
        scrollArea.setWindowTitle(_translate("scrollArea", "ScrollArea"))
        self.pushNewRow.setText(_translate("scrollArea", "新規登録"))
        self.pushSearch.setText(_translate("scrollArea", "検索"))
        self.lineSh2.setText(_translate("scrollArea", "aaaaa"))
        self.pushButtonWrite.setText(_translate("scrollArea", "書き込み"))
        self.labelSh1.setText(_translate("scrollArea", "入力先シート"))
        self.labelSh2.setText(_translate("scrollArea", "プルタブ参照シート"))
        self.pushButtonCancel.setText(_translate("scrollArea", "キャンセル"))
        self.pushQuit.setText(_translate("scrollArea", "終了"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    scrollArea = QtWidgets.QScrollArea()
    ui = Ui_scrollArea()
    ui.setupUi(scrollArea)
    scrollArea.show()
    sys.exit(app.exec_())

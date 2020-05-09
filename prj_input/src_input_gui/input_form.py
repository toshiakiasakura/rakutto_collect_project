import sys
import _utils 
from openpyxl import Workbook
from openpyxl import load_workbook

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,\
            QFileDialog, QMessageBox,QPushButton, QComboBox,\
            QLabel, QVBoxLayout, QHBoxLayout, QInputDialog,\
            QGridLayout, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QGuiApplication, QColor
import types 



path = "./test_data.xlsx"
shName1 = "患者情報入力シート"
shName2 = "患者プルタブシート" 

tpNumeric = "数値" 

class Ui_scrollArea(object):
    def __init__(self):
        self.row = 3
        self.baseRow = 2

    def initialize(self, scrollArea):
        self.setupGUI(scrollArea)


    def readData(self, path):
        self.wb = load_workbook(path)
        self.ws1 = self.wb[shName1]
        self.ws2 = self.wb[shName2] 

        self.maxRow = self.ws1.max_row
        self.maxColumn = self.ws1.max_column


    def setupGUI(self,scrollArea):
        scrollArea.setObjectName("scrollArea")
        mainWidth = 1000
        mainHeight = 600
        scrollArea.resize(mainWidth, mainHeight)
        scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollVerticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollVerticalLayout.setObjectName("scrollVerticalLayout")
        self.verticalLayoutScroll = QVBoxLayout()
        self.verticalLayoutScroll.setObjectName("verticalLayoutScroll")

        self.setupGridLayoutTop()
        self.setupScrollMiddle()
        self.setupGridLayoutBottom()
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.retranslateUi(scrollArea)

        QtCore.QMetaObject.connectSlotsByName(scrollArea)


    def displayRow(self):
        num  = _utils.checkNumeric( self.lineRow.text() ) 
        if isinstance( num, int):
            num += 1 
        print(num)
        self.lineRow.setText(str(num) ) 

    def setupGridLayoutTop(self):
        self.gridLayoutTop = QGridLayout()
        self.gridLayoutTop.setObjectName("gridLayoutTop")

        # lineRow
        self.lineRow = QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineRow.sizePolicy().hasHeightForWidth())
        self.lineRow.setSizePolicy(sizePolicy)
        self.lineRow.setMinimumSize(QtCore.QSize(50, 0))

        self.lineRow.setObjectName("lineRow")
        self.lineRow.setText( str(self.row) )
        self.lineRow.editingFinished.connect(self.displayRow)

        self.gridLayoutTop.addWidget(self.lineRow, 0, 0, 1, 1)

        self.comboRef1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboRef1.setObjectName("comboRef1")
        self.gridLayoutTop.addWidget(self.comboRef1, 0, 2, 1, 1)
        self.comboRef2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboRef2.setObjectName("comboRef2")
        self.gridLayoutTop.addWidget(self.comboRef2, 1, 2, 1, 1)
        spacerItem = QSpacerItem(50, 50, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 0, 1, 1, 1)


        self.lineRef1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef1.setObjectName("lineRef1")
        self.gridLayoutTop.addWidget(self.lineRef1, 0, 3, 1, 1)
        self.lineSearch = QLineEdit(self.scrollAreaWidgetContents)
        self.lineSearch.setObjectName("lineSearch")
        self.gridLayoutTop.addWidget(self.lineSearch, 0, 5, 1, 1)
        self.lineRef2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef2.setObjectName("lineRef2")
        self.gridLayoutTop.addWidget(self.lineRef2, 1, 3, 1, 1)
        self.comboSearch = QComboBox(self.scrollAreaWidgetContents)
        self.comboSearch.setObjectName("comboSearch")
        self.gridLayoutTop.addWidget(self.comboSearch, 0, 4, 1, 1)
        self.pushNewRow = QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushNewRow.sizePolicy().hasHeightForWidth())
        self.pushNewRow.setSizePolicy(sizePolicy)
        self.pushNewRow.setObjectName("pushNewRow")
        self.gridLayoutTop.addWidget(self.pushNewRow, 1, 0, 1, 1)
        self.pushSearch = QPushButton(self.scrollAreaWidgetContents)
        self.pushSearch.setObjectName("pushSearch")
        self.gridLayoutTop.addWidget(self.pushSearch, 1, 4, 1, 2)

        self.verticalLayoutScroll.addLayout(self.gridLayoutTop)

    def setupScrollMiddle(self):
        self.scrollMiddle = QScrollArea(self.scrollAreaWidgetContents)
        self.scrollMiddle.setWidgetResizable(True)
        self.scrollMiddle.setObjectName("scrollMiddle")
        self.scrollMiddle.setMinimumSize(QtCore.QSize(500,300)) 
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")

        self._horizontals = []
        self._labels = []
        self._comboBoxes = []
        self._lines = []
        self._horizontalSpacers = []

        for i in range(1, self.maxColumn+1 ):
            # check set new horizontal layout or not 
            colName = self.ws1.cell(self.baseRow, i).value 
            colName = _utils.checkStr(colName)
            if colName == "":
                continue
            self.setupMacros(i,colName)

        self.scrollMiddle.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutScroll.addWidget(self.scrollMiddle)

    def setupMacros(self,i,colName):
        self.horizontalLayoutMacro = QHBoxLayout()
        self.horizontalLayoutMacro.setObjectName("horizontalLayoutMacro")

        # labelMacro
        self.labelMacro = QLabel(self.scrollAreaWidgetContents_2)
        self.labelMacro.setObjectName("labelMacro")
        self.labelMacro.setMinimumSize(QtCore.QSize(150,0)) 

        self.labelMacro.setText( colName )
        
        self.horizontalLayoutMacro.addWidget(self.labelMacro)

        # comboBox setting.
        self.comboBoxMacro = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboBoxMacro.setObjectName("comboBoxMacro")
        self.comboBoxMacro.setMinimumSize(QtCore.QSize(150,0)) 
        self.comboBoxMacro.addItems( ["a","b","c"] ) 
        # initial color 
        
        self.comboBoxMacro.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,152,152);")

        def changeBack(self,s):
            ''' if compare with originla data and find difference, 
            change color '''
            self.setStyleSheet("background-color: rgb(255,255,0);color:rgb(0,152,152);")
        self.comboBoxMacro.changeBack = types.MethodType(changeBack,self.comboBoxMacro)
        self.comboBoxMacro.activated[str].connect(self.comboBoxMacro.changeBack)

        self.horizontalLayoutMacro.addWidget(self.comboBoxMacro)

        # lineEdit setting. 
        self.lineMacro = QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineMacro.setObjectName("lineMacro")
        self.lineRow.setMinimumSize(QtCore.QSize(150,0)) 
        self.horizontalLayoutMacro.addWidget(self.lineMacro)

        horizontalSpacerMacro = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # set object. 
        self.horizontalLayoutMacro.addItem(horizontalSpacerMacro)
        self.verticalLayout.addLayout(self.horizontalLayoutMacro)
        # add each objects. 
        self._horizontals.append(self.horizontalLayoutMacro)
        self._labels.append(self.labelMacro)
        self._comboBoxes.append(self.comboBoxMacro)
        self._lines.append(self.labelMacro)
        self._horizontalSpacers.append(self.horizontalLayoutMacro)

    def setupGridLayoutBottom(self):
        self.gridLayoutBottom = QGridLayout()
        self.gridLayoutBottom.setObjectName("gridLayoutBottom")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayoutBottom.addItem(spacerItem2, 0, 2, 1, 1)
        self.pushButtonWrite = QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonWrite.sizePolicy().hasHeightForWidth())
        self.pushButtonWrite.setSizePolicy(sizePolicy)
        self.pushButtonWrite.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButtonWrite.setObjectName("pushButtonWrite")
        self.gridLayoutBottom.addWidget(self.pushButtonWrite, 1, 3, 1, 1)

        # label1
        self.labelSh1 = QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSh1.sizePolicy().hasHeightForWidth())
        self.labelSh1.setSizePolicy(sizePolicy)
        self.labelSh1.setObjectName("labelSh1")
        self.gridLayoutBottom.addWidget(self.labelSh1, 0, 0, 1, 1)

        # label2 
        self.labelSh2 = QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSh2.sizePolicy().hasHeightForWidth())
        self.labelSh2.setSizePolicy(sizePolicy)
        self.labelSh2.setObjectName("labelSh2")
        self.gridLayoutBottom.addWidget(self.labelSh2, 1, 0, 1, 1)

        # lineSh1
        self.lineSh1 = QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSh1.sizePolicy().hasHeightForWidth())
        self.lineSh1.setSizePolicy(sizePolicy)
        self.lineSh1.setMinimumSize(QtCore.QSize(100, 0))
        self.lineSh1.setObjectName("lineSh1")
        self.lineSh1.setText(shName1)
        self.lineSh1.setEnabled(False) 
        self.gridLayoutBottom.addWidget(self.lineSh1, 0, 1, 1, 1)

        # lineSh2 
        self.lineSh2 = QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSh2.sizePolicy().hasHeightForWidth())
        self.lineSh2.setSizePolicy(sizePolicy)
        self.lineSh2.setObjectName("lineSh2")
        self.lineSh2.setText(shName2)
        self.lineSh2.setEnabled(False) 
        self.gridLayoutBottom.addWidget(self.lineSh2, 1, 1, 1, 1)


        self.pushButtonCancel = QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayoutBottom.addWidget(self.pushButtonCancel, 1, 4, 1, 1)


        # pushQuit 
        self.pushQuit = QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushQuit.sizePolicy().hasHeightForWidth())
        self.pushQuit.setSizePolicy(sizePolicy)
        self.pushQuit.setMinimumSize(QtCore.QSize(100, 0))
        self.pushQuit.setObjectName("pushQuit")

        self.pushQuit.clicked.connect(self.quitProcess)
        self.gridLayoutBottom.addWidget(self.pushQuit, 1, 5, 1, 1)


        self.verticalLayoutScroll.addLayout(self.gridLayoutBottom)
        self.scrollVerticalLayout.addLayout(self.verticalLayoutScroll)

    def quitProcess(self):
        # preFinishProcess()
        QApplication.instance().quit()

    def closeEvent(self, event):
        # preFinishProcess()
        event.accept()

    def retranslateUi(self, scrollArea):
        _translate = QtCore.QCoreApplication.translate
        scrollArea.setWindowTitle(_translate("scrollArea", "ScrollArea"))
        self.pushNewRow.setText(_translate("scrollArea", "新規登録"))
        self.pushSearch.setText(_translate("scrollArea", "検索"))
        self.pushButtonWrite.setText(_translate("scrollArea", "書き込み"))
        self.labelSh1.setText(_translate("scrollArea", "入力先シート"))
        self.labelSh2.setText(_translate("scrollArea", "プルタブ参照シート"))
        self.pushButtonCancel.setText(_translate("scrollArea", "キャンセル"))
        self.pushQuit.setText(_translate("scrollArea", "終了"))


def main():
    app = QApplication(sys.argv)

    scrollArea = QScrollArea()
    ui = Ui_scrollArea()
    ui.readData(path)

    ui.initialize(scrollArea)

    scrollArea.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

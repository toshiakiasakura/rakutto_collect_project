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
import inspect



path = "./test_data.xlsx"
shName1 = "患者情報入力シート"
shName2 = "患者プルタブシート" 

tpNumeric = "数値" 

class Ui_scrollArea():
    def __init__(self):
        self.row = 3
        self.baseRow = 2
        self.filter = [4,5,6]
        self.questionTitle = "confirmation"

    def initialize(self, scrollArea):
        self.setupGUI(scrollArea)


    def readData(self, path):
        self.wb = load_workbook(path)
        self.ws1 = self.wb[shName1]
        self.ws2 = self.wb[shName2] 

        self.maxRow = self.ws1.max_row
        self.maxRow2 = self.ws2.max_row
        self.maxColumn = self.ws1.max_column
        self.maxColumn2 = self.ws2.max_column

        # set colNameDic 
        self.colNameDic = {}
        self.colNameDic2 = {}
        self.indNameDic = {}
        for i in range(1,self.maxRow + 1 ): 
            colName = self.ws1.cell(self.baseRow, i).value 
            colName = _utils.checkStr(colName)
            if colName == "" or i in self.filter:
                continue
            self.colNameDic[colName] = i 

        for k,v in self.colNameDic.items():
            self.indNameDic[v] = k 

        for col in range(1, self.maxColumn2 + 1) :
            v = self.ws2.cell(self.baseRow, col).value
            v = _utils.checkStr( v ) 
            if v in self.colNameDic.keys() :
                self.colNameDic2[v] = col
        
    
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


    def changeRowRelated(self):
        num  = _utils.checkNumeric( self.lineRow.text() ) 
        if isinstance( num, int):
            num += 1 
            self.row = num
        else:
            raise Exception("not int value is inputted")

        print(num)
        print(self.ws1.max_row)
        self.lineRow.setText(str(num) ) 

        # change values 
        self.changeLineRef1( self.comboRef1.currentText() ) 
        self.changeLineRef2( self.comboRef2.currentText() ) 
        self.changeMacroValues()

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
        self.lineRow.editingFinished.connect(self.changeRowRelated)

        self.gridLayoutTop.addWidget(self.lineRow, 0, 0, 1, 1)


        horizontalSpacerTop= QSpacerItem(50, 50, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.gridLayoutTop.addItem(horizontalSpacerTop, 0, 1, 1, 1)

        # comboRef1
        self.comboRef1 = QComboBox(self.scrollAreaWidgetContents)
        self.comboRef1.setObjectName("comboRef1")
        self.comboRef1.addItems( self.colNameDic.keys() ) 
        self.comboRef1.activated[str].connect(self.changeLineRef1)        
        self.gridLayoutTop.addWidget(self.comboRef1, 0, 2, 1, 1)

        # comboRef2 
        self.comboRef2 = QComboBox(self.scrollAreaWidgetContents)
        self.comboRef2.setObjectName("comboRef2")
        self.comboRef2.addItems( self.colNameDic.keys() ) 
        self.comboRef2.setCurrentIndex(1)
        self.comboRef2.activated[str].connect(self.changeLineRef2)        
        self.gridLayoutTop.addWidget(self.comboRef2, 1, 2, 1, 1)

        # lineRef1 
        self.lineRef1 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef1.setObjectName("lineRef1")
        val =  self.getValueFromColumn( self.comboRef1.currentText() ) 
        self.lineRef1.setText(val)
        self.lineRef1.setEnabled(False) 
        self.gridLayoutTop.addWidget(self.lineRef1, 0, 3, 1, 1)

        # lineRef2
        self.lineRef2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineRef2.setObjectName("lineRef2")
        val =  self.getValueFromColumn( self.comboRef2.currentText() ) 
        self.lineRef2.setText(val)
        self.lineRef2.setEnabled(False) 
        self.gridLayoutTop.addWidget(self.lineRef2, 1, 3, 1, 1)

        # comboSearch 
        self.comboSearch = QComboBox(self.scrollAreaWidgetContents)
        self.comboSearch.addItems( self.colNameDic.keys() ) 
        self.comboSearch.setObjectName("comboSearch")
        self.comboSearch.activated[str].connect(self.changeLineSearch)        
        self.gridLayoutTop.addWidget(self.comboSearch, 0, 4, 1, 1)

        # lineSearch 
        self.lineSearch = QLineEdit(self.scrollAreaWidgetContents)
        self.lineSearch.setObjectName("lineSearch")
        val =  self.getValueFromColumn( self.comboSearch.currentText() ) 
        self.lineSearch.setText(val)
        self.gridLayoutTop.addWidget(self.lineSearch, 0, 5, 1, 1)

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

        for colName in self.colNameDic.keys():
            # check set new horizontal layout or not 
            self.setupMacros(colName)

        self.scrollMiddle.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutScroll.addWidget(self.scrollMiddle)

    def setupMacros(self,colName):
        self.horizontalLayoutMacro = QHBoxLayout()
        self.horizontalLayoutMacro.setObjectName("horizontalLayoutMacro")

        # labelMacro
        self.labelMacro = QLabel(self.scrollAreaWidgetContents_2)
        self.labelMacro.setObjectName("labelMacro")
        self.labelMacro.setMinimumSize(QtCore.QSize(150,0)) 
        self.labelMacro.setText( colName )
        self.horizontalLayoutMacro.addWidget(self.labelMacro)


        # lineEdit setting. 
        self.lineMacro = QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineMacro.setObjectName("lineMacro")
        self.lineMacro.setMinimumSize(QtCore.QSize(150,0)) 
        self.lineMacro.setStyleSheet(
                "QLineEdit { background-color : white; color:rgb(0,60,60)}")
        self.lineMacro.colName = colName 
        self.lineMacro._same = False 
        def changeBack(selfMacro ):
            b = self.compareValue( selfMacro.text() , selfMacro.colName ) 
            selfMacro._same = b
            if b:
                selfMacro.setStyleSheet(
                "QLineEdit { background-color : white; color:rgb(0,60,60)}")

            else:
                selfMacro.setStyleSheet(
                "QLineEdit { background-color : yellow ; color:rgb(0,60,60)}")
        self.lineMacro.changeBack = types.MethodType(changeBack,self.lineMacro)
        self.lineMacro.editingFinished.connect( self.lineMacro.changeBack )

        v = self.getValueFromColumn(self.labelMacro.text() ) 
        self.lineMacro.setText( v ) 

        self.horizontalLayoutMacro.addWidget(self.lineMacro)

        # comboBox setting.
        self.comboBoxMacro = QComboBox(self.scrollAreaWidgetContents_2)
        self.comboBoxMacro.setObjectName("comboBoxMacro")
        self.comboBoxMacro.setMinimumSize(QtCore.QSize(150,0)) 
        lis_ = self.getItemsFromSheet2(colName) 
        self.comboBoxMacro.addItems( lis_ ) 
        self.comboBoxMacro.colName = colName
        self.comboBoxMacro.defaultItems = lis_ 
        self.comboBoxMacro.line = self.lineMacro
        # initial color 
        self.comboBoxMacro.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,0,0);")

        def changeBack(selfMacro):
            v = selfMacro.currentText()
            selfMacro.line.setText( v ) 

            b = self.compareValue( v , selfMacro.colName ) 
            selfMacro.line._same = b
            if b:
                selfMacro.setStyleSheet(
                "background-color : white; color:rgb(0,60,60)")
            else:
                selfMacro.setStyleSheet(
                "background-color : yellow ; color:rgb(0,60,60)")

        self.comboBoxMacro.changeBack = types.MethodType(changeBack,self.comboBoxMacro)
        self.comboBoxMacro.activated[str].connect(self.comboBoxMacro.changeBack)

        self.horizontalLayoutMacro.addWidget(self.comboBoxMacro)

        # spacer  setting 
        horizontalSpacerMacro = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayoutMacro.addItem(horizontalSpacerMacro)
        self.verticalLayout.addLayout(self.horizontalLayoutMacro)
        # add each objects. 
        self._horizontals.append(self.horizontalLayoutMacro)
        self._labels.append(self.labelMacro)
        self._comboBoxes.append(self.comboBoxMacro)
        self._lines.append(self.lineMacro)
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

    def quitProcess(self):
        print( inspect.currentframe().f_code.co_name) 
        reply = self.preFinishProcess()
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
        else:
            pass 

    def closeEvent(self, event):
        # dose not work well.
        self.preFinishProcess()
        event.accept()

    def preFinishProcess(self):
        print( inspect.currentframe().f_code.co_name) 
        flag = self.checkDiffExist()
        reply = QMessageBox.No
        if flag :
            exp1 = "現在、変更されている変更は保存されません。よろしいでしょうか。" 
            print(exp1)
            reply = QMessageBox.question(self.scrollAreaWidgetContents, self.questionTitle,exp1, 
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return(reply)



    def changeMacroValues(self):
        for i in range(len(self._lines) ) :
            # line setting 
            v = self.getValueFromColumn( self._labels[i].text() ) 
            self._lines[i].setText(v)  
            # comboBox setting 
            self._comboBoxes[i].clear()
            self._comboBoxes[i].addItems( self._comboBoxes[i].defaultItems ) 
            if v not in self._comboBoxes[i].defaultItems:
                self._comboBoxes[i].insertItem(0,v)

    def checkDiffExist(self):
        flag = False
        for i in range( len(self._lines) ) :
            if not self._lines[i]._same:
                flag = True
                return(flag)
        return(flag) 


    def changeLineRef1(self,s ) :
        v = self.getValueFromColumn(s)
        self.lineRef1.setText(v) 

    def changeLineRef2(self,s ) :
        v = self.getValueFromColumn(s)
        self.lineRef2.setText(v) 

    def changeLineSearch(self, s):
        v = self.getValueFromColumn(s)
        self.lineSearch.setText(v)

    def compareValue(self, v,colName):
        colInd = self.colNameDic[colName]
        origV = self.ws1.cell(self.row, colInd).value
        origV = _utils.checkStr(origV) 
        if v == origV:
            return(True)
        else:
            return(False)


    def getItemsFromSheet2(self, colName):
        index = self.colNameDic2.get(colName, None)
        if index == None:
            return([])
        lis_ = []
        for row in range(self.baseRow + 1 , self.maxRow + 1 ):
            v = self.ws2.cell( row, index).value
            v = _utils.checkStr(v) 
            if v == "":
                return(lis_) 
            lis_.append(v)
        return(lis_)


    def getAllItemsCombo(self,combo):
        lis_ = []
        for i in range(combo.count()):
            lis_.append( combo.itemText(i) ) 
        return( lis_) 

    def getValueFromColumn(self,colName):
        colInd = self.colNameDic.get(colName ,None) 
        if colInd == None:
            print("Error there is no column name") 
            v = "eeeeerrrr"
        else:
            v = self.ws1.cell(self.row,colInd).value  
            v = _utils.checkStr(v) 
        return(v) 

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

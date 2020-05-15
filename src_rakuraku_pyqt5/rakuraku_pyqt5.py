# ======================================================================
# Project Name    : rakutto_collect_project
# File Name       : rakuraku_pyqt5.py
# Encoding        : utf-8
# Copyright © 2020 Toshiaki Asakura. All rights reserved.
# ======================================================================
# 
# TO DO LIST: 
#

import sys
import os
import time
import pandas as pd 
import numpy as np 
import datetime 
import textwrap

import _utils
import pathList as pL

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,\
            QFileDialog, QMessageBox,QPushButton, QComboBox,\
            QLabel, QVBoxLayout, QInputDialog
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtTest import QTest

comboItem1   = "診断検査の集計"
comboItem2   = "新型コロナウイルス感染患者入院状況"
comboItem4   = "患者発生状況の集計"
comboItem5   = "table7" 
comboItem6   = "陽性者の属性別層別集計"
comboItem8   = "突合-患者・検査データ" 
comboItem9   = "A4フォーマットの出力"
comboItem10  = "単純な感染患者入院状況"
comboItem11  = "複数の患者データの突合" 
comboItem12  = "送付用のデータの作成" 
comboItem13  = "検査機関からのデータを検査データに挿入"
comboItem14  = "患者データの日付集計-層別集計"
comboItem15  = "入力規則の延長"
comboItem16  = "積極的疫学調査調査票データ抜き出しプログラム" 
comboItem17  = "患者データの入力フォーム" 

comboItemAll = "全実行"
comboItemPatientAll = "全実行(患者データからのみ)"
comboItemError = "未実装"

comboItems = [ comboItemPatientAll, comboItem13, comboItem12,
        comboItem11, comboItem9, comboItem10, 
        comboItem4, comboItem1, comboItem8 , comboItem2 ,
        comboItem5, comboItem6, comboItem14,
        comboItem15, comboItem16, comboItem17, 
        comboItemAll, comboItemError ] 

comboExp1= '''【実行するプログラムの説明】
< 検査データの集計 >
検査データに関して集計を行います。
 
'''

comboExp2 = '''【実行するプログラムの説明】
< 突合プログラム >
新型コロナウイルス感染患者入院状況を　
2つのファイルから作成します。

'''


comboExp4 = '''【実行するプログラムの説明】
< 患者データの集計> 
孤発、初発、後発の集計を行います。
身体状況（現在の症状）の集計。
入院の有無（入院日より）、退院の有無の集計、
この二つより現在入院患者数を算出します。

'''

comboExp5 = '''【実行するプログラムの説明】
< 患者データの集計> 
出力はtable7 です。

'''

comboExp6 = '''【実行するプログラムの説明】
< 患者データの集計> 
確定日(公表)から、基本情報を集計します。
保健所、年齢、性別、日付、
日付-保健所 、日付-保健所-累積、
で層別化された結果が集計されます。　 

'''


comboExp8 = '''【実行するプログラムの説明】
< 突合プログラム> 
陽性確認日、陰性確認開始日、陰性確認日を検査データから更新します。

'''

comboExp9 = '''【実行するプログラムの説明】
< 変換プログラム > 
A4で印刷出来るexcelの形で出力します。

'''

comboExp10 = '''【実行するプログラムの説明】
< 変換プログラム > 
患者データのみから新型コロナウイルス感染患者入院状況の
フォーマットへ変換を行います。

'''

comboExp11 = '''【実行するプログラムの説明】
< 突合プログラム > 
複数の患者データを突合します。
同じ患者データが各ファイルに
含まれないように気をつけてください。
'''

comboExp12 = '''【実行するプログラムの説明】
< 変換プログラム > 
非公表のデータに入っているデータを削除します。
また、項目名に"*"が入っている項目を削除します。

'年代：公表の可否' : '年代'
'性別：公表の可否' : '性別'
'居住地：公表の可否' :  '居住地', '居住地２'
'職業：公表の可否' : '職業分類', '職業２', '職業：備考'
'発症日：公表の可否' : '発症日' 
'''

items = [ x.replace("\n","") for x in pL.insertCols] 
items = "\n".join(textwrap.wrap( ",  ".join(items) ,50) )
comboExp13 = f'''【実行するプログラムの説明】
< 挿入プログラム > 
以下の項目を検査機関のデータから
検査データに挿入します。
現在は、常に全て上書きされるようになっています。

{items}
'''

comboExp14 = '''【実行するプログラムの説明】
< 集計プログラム > 
日付ごとの集計。
層別の集計。

'''

comboExp15 = '''【実行するプログラムの説明】
< 編集プログラム > 
入力規則の延長

'''

comboExp16 = '''【実行するプログラムの説明】
< 変換プログラム > 
複数の積極的疫学調査調査票のファイルから、
臨床情報、接触者情報を抜き出します。

'''

comboExp17 = '''【実行するプログラムの説明】
< 入力補助プログラム > 
入力フォームです。
初めて使う人は、入力フォームのヘルプを確認してください。
'''

comboExpAll = f'''【実行するプログラムの説明】
< 全実行 > 
このプログラムでは以下の順番で処理が行われます。
- {comboItem1} 
- {comboItem8}
- {comboItem6}
- {comboItem4}
- {comboItem5}
- {comboItem9} 
'''

comboExpPatientAll = f'''【実行するプログラムの説明】
< 全実行 > 
このプログラムでは以下の順番で処理が行われます。
- {comboItem4}
- {comboItem9}
- {comboItem10}
- {comboItem14}

'''



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = '楽々集計プログラム'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

        self.ex_list = []
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initItems()
        self.initCombo()
        self.initFileAndActivationButton()
        self.initQuitButton()

        self.adjustLayout()
        self.show()

    def initItems(self):
        self.Items = {}
        patientFileChocie = self.fileChoiceItem6

        self.Items[comboItem1] = {"comboExp": comboExp1,
                "fileChoice":self.fileChoiceItem1,
                "run":self.runItem1}

        self.Items[comboItem2] = {"comboExp": comboExp2,
                "fileChoice": self.fileChoiceItem2,
                "run":self.runItem2}

        self.Items[comboItem4] = {"comboExp": comboExp4,
                "fileChoice": patientFileChocie,
                "run":self.runItem4}

        self.Items[comboItem5] = {"comboExp": comboExp5,
                "fileChoice": patientFileChocie,
                "run":self.runItem5}

        self.Items[comboItem6] = {"comboExp": comboExp6,
                "fileChoice": patientFileChocie,
                "run":self.runItem6}

        self.Items[comboItem8] = {"comboExp": comboExp8,
                "fileChoice":self.fileChoiceItem8,
                "run":self.runItem8}

        self.Items[comboItem9] = {"comboExp": comboExp9,
                "fileChoice": patientFileChocie,
                "run":self.runItem9}

        self.Items[comboItem10] = {"comboExp": comboExp10,
                "fileChoice": patientFileChocie,
                "run":self.runItem10}

        self.Items[comboItem11] = {"comboExp": comboExp11,
                "fileChoice": self.fileChoiceItem11,
                "run":self.runItem11}

        self.Items[comboItem12] = {"comboExp": comboExp12,
                "fileChoice": patientFileChocie,
                "run":self.runItem12}

        self.Items[comboItem13] = {"comboExp": comboExp13,
                "fileChoice": self.fileChoiceItem13,
                "run":self.runItem13}

        self.Items[comboItem14] = {"comboExp": comboExp14,
                "fileChoice": patientFileChocie,
                "run":self.runItem14}

        self.Items[comboItem15] = {"comboExp": comboExp15,
                "fileChoice": self.fileChoiceItem1,
                "run":self.runItem15}

        self.Items[comboItem16] = {"comboExp": comboExp16,
                "fileChoice": self.fileChoiceItem16,
                "run":self.runItem16}

        self.Items[comboItem17] = {"comboExp": comboExp17,
                "fileChoice": patientFileChocie,
                "run":self.runItem17}

        self.Items[comboItemAll] = {"comboExp": comboExpAll,
                "fileChoice":self.fileChoiceItemAll,
                "run":self.runItemAll}

        self.Items[comboItemPatientAll] = {"comboExp": comboExpPatientAll,
                "fileChoice": patientFileChocie,
                "run":self.runItemPatientAll }

        self.Items[comboItemError] = {}

    def initCombo(self):
        self.combo = QComboBox(self)
        for c in comboItems:
            self.combo.addItem(c)

        comSt = self.Items[comboItems[0]]["comboExp"]
        self.lbl = QLabel(comSt, self)

        self.combo.activated[str].connect(self.comboActivate)

    def comboActivate(self, text):
        comText = self.combo.currentText()

        comboExp = self.Items[comText].get("comboExp",None) 
        status = self.Items[comText].get("status","待機中")

        self.lbl.setText(comboExp)
        self.statusLbl.setText(status )

        self.lbl.adjustSize()
        self.statusLbl.adjustSize()

        self.initFileNames()

    def initFileAndActivationButton(self):
        self.fileBtn= QPushButton('ファイル選択', self)
        self.fileBtn.clicked.connect(self.fileChoicePattern)
        self.fileLbl = QLabel("選択したファイル : ", self)
        # define fileNames 
        self.initFileNames()

        self.runBtn = QPushButton("実行", self) 
        self.runBtn.clicked.connect(self.runProgram)

        self.statusLbl = QLabel("未実行", self)

    def initFileNames(self):
        self.fileName  = ""
        self.fileName1 = ""
        self.fileName2 = ""
        self.fileName3 = ""
        self.fileNames = []

        self.fileFlag  = False
        self.fileLbl.setText("選択したファイル :")

    def fileChoicePattern(self):
        self.questionTitle = "選択ファイルの確認"
        comText = self.combo.currentText()
        callFileChoice= lambda x : self.Items[x].get("fileChoice",self.fileChoiceError)()
        callFileChoice(comText)
        self.fileLbl.repaint()

        
    def fileChoiceItem1(self):
        exp1  = "検査データ を選択してください。"
        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileName = self.openFileNameDialog()

        fN = self.fileName.split("/")[-1]
        text = f"選択したファイル :\n {fN}"
        self.fileExtentionCheck()
        self.fileLbl.setText(text)

    def fileChoiceItem2(self):
        exp1 = "患者データ を選択してください。"
        exp2 = "病院病床データ を選択してください。"

        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileName1 = self.openFileNameDialog()

        QMessageBox.question(self, self.questionTitle, exp2, QMessageBox.Yes)
        self.fileName2 = self.openFileNameDialog()

        self.fileExtentionCheck(pattern="two")

        text = f"< 患者データ > \n {self.fileName1}\n"
        text += f"< 医療圏 >\n {self.fileName2}"
        self.fileLbl.setText(text)


    def fileChoiceItem6(self):
        exp1  = "患者データ を選択してください。"
        QMessageBox.question(self, self.questionTitle, exp1, QMessageBox.Yes)

        self.fileName = self.openFileNameDialog()
        fN = self.fileName.split("/")[-1]
        text = f"< 患者データ > \n {fN}"
        self.fileExtentionCheck()
        self.fileLbl.setText(text)


    def fileChoiceItem8(self):
        exp1 = "患者データ を選択してください。"
        exp2  = "検査データ を選択してください。"

        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileName1 = self.openFileNameDialog()

        QMessageBox.question(self, self.questionTitle, exp2, QMessageBox.Yes)
        self.fileName2 = self.openFileNameDialog()

        self.fileExtentionCheck(pattern="two")
        
        fN1 = self.fileName1.split("/")[-1]
        fN2 = self.fileName2.split("/")[-1]
        text = f"< 患者データ >\n {fN1}\n"
        text += f"< 検査データ >\n {fN2}"
        self.fileLbl.setText(text)

    def fileChoiceItem11(self):
        exp1 = "突合するデータを複数、選択してください。"

        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileNames = self.openFileNamesDialog()

        self.fileExtentionCheck(pattern="multiple")
        text = f"< 患者データ > \n"
        fNs = [ x.split("/")[-1] for x in self.fileNames ]
        text += "\n".join(fNs)
        self.fileLbl.setText(text)

    def fileChoiceItem13(self):
        exp1 = "データ挿入先の検査データを、選択してください。"
        exp2 = "検査機関データを、選択してください。"

        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileName = self.openFileNameDialog()

        QMessageBox.question(self, self.questionTitle,exp2, QMessageBox.Yes)
        self.fileNames = self.openFileNamesDialog()

        self.fileExtentionCheck(pattern="multiple")
        text = f"< 検査データ > \n"
        fN = self.fileName.split("/")[-1]
        text += f"{fN}\n"
        text += "< 検査機関データ >\n"
        fNs = [ x.split("/")[-1] for x in self.fileNames ]
        text += "\n".join(fNs)
        self.fileLbl.setText(text)

    def fileChoiceItem16(self):
        exp1  = "積極的疫学調査調査票が入ったディレクトリー を選択してください。"
        QMessageBox.question(self, self.questionTitle, exp1, QMessageBox.Yes)

        self.fileName = self.openDirectoryDialog()
        text = f"< ディレクトリー名 > \n {self.fileName}"
        self.fileLbl.setText(text)
        self.fileFlag = True

    def fileChoiceItemAll(self):
        exp1 = "患者データ を選択してください。"
        exp2 = "検査データ を選択してください。"
        exp3 = "病院病床一覧 を選択してください。"

        QMessageBox.question(self, self.questionTitle,exp1, QMessageBox.Yes)
        self.fileName1 = self.openFileNameDialog()

        QMessageBox.question(self, self.questionTitle, exp2, QMessageBox.Yes)
        self.fileName2 = self.openFileNameDialog()

        QMessageBox.question(self, self.questionTitle, exp3, QMessageBox.Yes)
        self.fileName3 = self.openFileNameDialog()

        self.fileExtentionCheck(pattern="three")
        text = f"< 患者データ > \n {self.fileName1}\n"
        text += f"< 検査データ > \n {self.fileName2}\n"
        text += f"病院病床一覧 :\n {self.fileName3}"

        self.fileLbl.setText(text)

    def fileChoiceError(self):
        text = '実装されていません'
        self.fileLbl.setText(text)

    def fileExtentionCheck(self, pattern="one"):
        if pattern=="one":
            if self.fileName.split(".")[-1] != "xlsx":
                self.fileFlag = False
            else:
                self.fileFlag = True
        elif pattern=="two":
            if (self.fileName1.split(".")[-1] != "xlsx") or (self.fileName2.split(".")[-1] != "xlsx"):
                self.fileFlag = False
            else:
                self.fileFlag = True
        elif pattern=="three" :
            if (self.fileName1.split(".")[-1] != "xlsx") or\
                (self.fileName2.split(".")[-1] != "xlsx") or\
                (self.fileName3.split(".")[-1] != "xlsx") :
                self.fileFlag = False
            else:
                self.fileFlag = True

        elif pattern=="multiple" : 
            self.fileFlag = True 
            for f in self.fileNames: 
                ext = f.split(".")[-1] 
                if ext != "xlsx":
                    self.fileFlag = False


    def runProgram(self):
        self.statusLbl.setText("実行中")
        self.statusLbl.repaint()
        QTest.qWait(0.5)

        self.errorMsg = ""
        
        # プログラムごとの対応
        if self.fileFlag:

            try:
                callRunProgram = lambda x : self.Items[x].get("run",self.runErorr)()
                callRunProgram( self.combo.currentText() )

                for f in [self.fileName,self.fileName1, self.fileName2, self.fileName3]:
                    if f:
                        _utils.createErrorCheckFile(f ,program = self.combo.currentText() )
            except:
                dir_ = _utils.getOutputDir()
                fileErrorRecord = "errorRecord.txt" 
                pathErorrRecord = dir_ + fileErrorRecord 

                self.errorMsg += "予期せぬエラーが発生しました。\n"
                self.errorMsg += f"{fileErrorRecord} にエラーを出力してます。"
                with open( pathErorrRecord, "w") as f :
                    import traceback
                    errorRecord =  traceback.format_exc()
                    f.write(errorRecord)
                
        else:
            self.errorMsg += ".xlsxのファイルを選択してから実行してください。" 

        self.runErrorCheck(self.errorMsg)
        self.statusLbl.repaint()


    def runItem1(self):
        # 集計
        self.readTest(self.fileName)

        if self.errorMsg == "":
            import test_totaling 
            test_totaling.diagnosticEngineering(self.test, self.fileName)

    def runItem2(self):
        self.readDF(self.fileName1) 
        self.readHospital(self.fileName2) 

        if self.errorMsg == "":
            import in_hosp_status
            in_hosp_status.mergeProcessFiles(self.df, self.hospital)

    def runItem4(self):
        self.readDF(self.fileName)

        if self.errorMsg == "":
            import patient_info_totaling
            patient_info_totaling.tableProcessing(self.df, self.fileName)

    def runItem5(self):
        self.readDF(self.fileName)

        if self.errorMsg == "":
            import patient_daily_totaling
            patient_daily_totaling.tableProcessing(self.df,self.fileName)

    def runItem6(self):
        self.readDF(self.fileName)

        if self.errorMsg == "":
            # TO DO, change for not using pullDown 
            import patient_basic_info
            patient_basic_info.diagnosticEngineering(self.df,self.df,self.fileName)


    def runItem8(self):
        self.readDF(self.fileName1)
        self.readTest(self.fileName2)

        if self.errorMsg == "":
            import merge_test_result
            merge_test_result.mergeTest(self.df,self.test, self.fileName1)

    def runItem9(self):
        self.readDF(self.fileName)

        if self.errorMsg == "":
            import output_A4_format
            output_A4_format.dataProcessing(self.df, self.fileName)

    def runItem10(self):
        self.readDF(self.fileName)

        if self.errorMsg == "":
            import simple_in_hosp_status
            simple_in_hosp_status.conversion(self.df, self.fileName)
            simple_in_hosp_status.formatExcelStyle(self.fileName)

    def runItem11(self):
        self.readDFs(self.fileNames)
        
        if self.errorMsg == "":
            import merge_multiple_patients
            res = merge_multiple_patients.mergeDFs(self.dfs, self.fileNames)

            if res: 
                exp  = res
                title = "注意!"
                QMessageBox.question(self ,title ,exp , QMessageBox.Yes)

    def runItem12(self):
        self.readDF(self.fileName)
        
        if self.errorMsg == "":
            password, ok = QInputDialog.getText(self, 'Input Dialog',
                'パスワードを入力してください。')

            if ok :
                import del_zip_crypt 
                del_zip_crypt.del_zip_crypt(self.df, self.fileName, password)
            else:
                self.errorMsg += "パスワードが設定されていません。"

    def runItem13(self):
        self.readTest(self.fileName)
        self.readTests(self.fileNames)
        
        if self.errorMsg == "":
            import auto_insert_testInst_data
            errorMsg = auto_insert_testInst_data.autoInsert(self.dfs, self.test, self.fileNames, self.fileName,)
            if errorMsg:
                self.errorMsg += errorMsg

            path = self.fileName 
            pathOutput = path[:-5] + "_追加済み.xlsx" 

            if not self.errorMsg:
                import extend_format
                extend_format.extendFormat(pathOutput,change=False)

    def runItem14(self):
        self.readDF(self.fileName)
        
        if self.errorMsg == "":
            import various_tabling
            various_tabling.daily_tabling(self.df,self.fileName)
            various_tabling.crossTabulation(self.df,self.fileName)


    def runItem15(self):
        self.readTest(self.fileName)
        
        if self.errorMsg == "":
            import extend_format
            extend_format.extendFormat(self.fileName)

    def runItem16(self):
        import nCoV_survey
        nCoV_survey.main(self.fileName)

    def runItem17(self):
        import input_form
        
        self.ex_list.append(
                input_form.Ui_scrollArea(
                    self.fileName, 
                    pL.patientSheetName, 
                    pL.patientPullName
                    )
                )

    def runItemAll(self):
        # read files 
        try:
            df, pullDown, test, hospital  = self.readFiles()
            _utils.createErrorCheckFile(self.fileName1,program = "全実行" )
            _utils.createErrorCheckFile(self.fileName2,program = "全実行" )
            _utils.createErrorCheckFile(self.fileName3,program = "全実行" )
        except:
            errorMsg = "予期せぬエラーが発生しました\n"
            import traceback
            errorMsg += traceback.format_exc()
            self.runErrorCheck(errorMsg)
            return()

        # run program one by one. 

        #import test_totaling 
        #test_totaling.diagnosticEngineering(test,self.fileName2)

        import merge_test_result
        merge_test_result.mergeTest(df,test,self.fileName1)

        dir_ = _utils.getOutputDir()
        pathNew = dir_ +  self.fileName1.split("/")[-1][:-5] + "_rep.xlsx"
        dfNew = pd.read_excel(pathNew,sheet_name = pL.patientSheetName,
                encoding="cp932",header=1) 

        import patient_basic_info
        patient_basic_info.diagnosticEngineering(dfNew,pullDown,pathNew)

        import in_hosp_status
        in_hosp_status.mergeProcessFiles(dfNew, hospital)
        in_hosp_status.formatExcelStyle()

        import simple_in_hosp_status
        simple_in_hosp_status.conversion(dfNew, pathNew)
        simple_in_hosp_status.formatExcelStyle(pathNew)

        import patient_info_totaling
        patient_info_totaling.tableProcessing(dfNew,pathNew)

        import patient_daily_totaling
        patient_daily_totaling.tableProcessing(dfNew,pathNew)

        import output_A4_format
        output_A4_format.dataProcessing(dfNew,pathNew)


    def runItemPatientAll(self):
        # read files 
        path = self.fileName

        self.readDF(path)
        if self.errorMsg != "":
            return()

        import simple_in_hosp_status
        simple_in_hosp_status.conversion(self.df, path)
        simple_in_hosp_status.formatExcelStyle(path)

        import patient_info_totaling
        patient_info_totaling.tableProcessing(self.df, path)

        import output_A4_format
        output_A4_format.dataProcessing(self.df, path)

        import various_tabling
        various_tabling.daily_tabling(self.df, path)
        various_tabling.crossTabulation(self.df, path)

    def readDF(self,path):
        try:
            self.df = pd.read_excel(path ,
                sheet_name = pL.patientSheetName, encoding="cp932",header=1) 
            self.df = self.df.dropna(axis=0,how="all")
            if self.df.shape[0] == 0:
                self.errorMsg += "データが入っていません。"
            self.addMissColumns(self.df, pL.patientColNames, path)
            
        except:    
            self.errorMsg += f"{pL.patientSheetName} のシートがありません。\n"
            self.errorMsg += f"または、読み込みに問題があります。\n"

    def readDFs(self,paths):
        try:
            self.dfs = []
            for path in paths:
                df = pd.read_excel(path ,
                    sheet_name = pL.patientSheetName, encoding="cp932",header=1) 
                df = df.dropna(axis=0,how="all")
                self.addMissColumns(df, pL.patientColNames, path)
                self.dfs.append(df)
            
        except:    
            self.errorMsg += f"{pL.patientSheetName} のシートがありません。\n"
            self.errorMsg += f"または、読み込みに問題があります。\n"

    def readTest(self,path):
        try:
            self.test = pd.read_excel(path ,
                sheet_name = pL.testSheetName, encoding="cp932",header=1) 
            self.test= self.test.dropna(axis=0,how="all")
            if self.test.shape[0] == 0:
                self.errorMsg += "データが入っていません。"
            self.addMissColumns(self.test, pL.testColNames , path)

        except:    
            self.errorMsg += f"{pL.testSheetName} のシートがありません。\n"
            self.errorMsg += f"または、読み込みに問題があります。\n"

    def readTests(self,paths):
        try:
            self.dfs = []
            for path in paths:
                df = pd.read_excel(path ,
                    sheet_name = pL.testSheetName, encoding="cp932",header=1) 
                df = df.dropna(axis=0,how="all")
                self.addMissColumns(df, pL.insertCols, path)
                self.dfs.append(df)
            
        except:    
            self.errorMsg += f"{pL.patientSheetName} のシートがありません。\n"
            self.errorMsg += f"または、読み込みに問題があります。\n"

    def readHospital(self,path):
        try:
            self.hospital = pd.read_excel(path ,
                sheet_name = pL.hospitalSheetName, encoding="cp932",header=0) 
            if self.hospital.shape[0] == 0:
                self.errorMsg += "データが入っていません。"
        except:    
            self.errorMsg += f"{pL.hospitalSheetName} のシートがありません。\n"
            self.errorMsg += f"または、読み込みに問題があります。\n"

    def addMissColumns(self,df_, lis_,path):
        miss = []
        for c in lis_:
            if c not in df_.columns:
                miss.append(c)
        
        if len(miss) > 0 : 
            fileName = path.split("/")[-1]
            self.errorMsg += f"{fileName} には以下のカラムがありません。改行も区別します。\n"
            s = ",".join(miss) 
            self.errorMsg +=  f"[{s}]"

    def readFiles(self):

        try:
            df = pd.read_excel(self.fileName1,
                    sheet_name = pL.patientSheetName, encoding="cp932",header=1) 
            pullDown = pd.read_excel(self.fileName1,
                    sheet_name=pL.patientPullName, encoding="cp932",header=1)

            test = pd.read_excel(self.fileName2, 
                    header = 1,  encodeing="cp932" ,sheet_name=pL.testSheetName)

            hospital = pd.read_excel(self.fileName3,encoding='cp932',sheet_name='Sheet1')
            hospital = hospital.replace(np.nan, '')
            return(df,pullDown, test,hospital)
        except:
            errorMsg = "データが読み込めませんでした。\n"
            import traceback
            errorMsg += traceback.format_exc()
            self.runErrorCheck(errorMsg)
            print(errorMsg)


    def runErrorCheck(self,errorMsg):
        if errorMsg == "":
            errorMsg = "実行終了"
        elif errorMsg == None:
            errorMsg = "実行終了or実装されていません"

        self.statusLbl.setText(errorMsg)

    def runErorr(self):
        text = '実装されていません'
        self.statusLbl.setText(text)


    def initQuitButton(self):
        self.qbtn = QPushButton('終了', self)
        # self.qbtn.clicked.connect(QApplication.instance().quit)        
        self.qbtn.clicked.connect(self.quitProcess)

    def quitProcess(self):
        preFinishProcess()
        QApplication.instance().quit()

    def adjustLayout(self):
        self.vbox = QVBoxLayout()

        self.qbtn.resize(100,100)
        self.vbox.addWidget(self.combo)
        self.vbox.addWidget(self.fileBtn)

        # labels 
        self.vbox.addWidget(self.lbl)
        self.vbox.addWidget(self.fileLbl)
        self.vbox.addWidget(self.statusLbl)
        self.vbox.addWidget(self.runBtn)
        self.vbox.addWidget(self.qbtn)

        self.setLayout(self.vbox)
        self.move(50,50)


    def checkFile(self,explanation):
        QMessageBox.question(self, "選択ファイルの確認",explanation,
                    QMessageBox.Yes)

    def checkProgram(self):
        reply = QMessageBox.question(self, 'Message',
            "このプログラムで合ってますか？", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        return(reply)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        return(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        return(files)

    def openDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(None,"QFileDialog.getExistingDirectory",options=options) 
        return(path)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def closeEvent(self, event):
        preFinishProcess()
        event.accept()

def preFinishProcess():
    dir_ = _utils.getOutputDir(create=False)
    
    if os.path.exists(dir_): 
        index = dir_.rfind("_") 
        dirNew = dir_[:index] + "_" +\
             datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        os.rename(dir_,dirNew)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# ======================================================================
# Project Name    : rakutto_collect_project
# File Name       : patient_basic_info.py
# Encoding        : utf-8
# Copyright © 2020 Toshiaki Asakura. All rights reserved.
# ======================================================================

import pandas as pd
import numpy as np
import datetime
import os
import sys
import pandas.tseries.offsets as offsets
import _utils

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

program = "patient_basic_info.py"

phcCol= '保健所'
ageCol = '年代'
sexCol = '性別'
testDateCol ='確定日（公表）' 
colList = [phcCol, ageCol, sexCol,testDateCol]


def main(path):
    try:
        df =pd.read_excel(path,sheet_name=pL.patientSheetName,
                encoding="cp932",header = 1)
        pullDown = pd.read_excel(path,sheet_name="プルタブシート",encoding="cp932",header = 1)
    except:
        errorMsg = "データが読み込めませんでした。\n"
        import traceback
        errorMsg  +=  traceback.format_exc()
        return(errorMsg)


    errorMsg = getErrorMsg(df,pullDown)
    if errorMsg == False:
        try:
            diagnosticEngineering(df,pullDown,path)
            _utils.createErrorCheckFile(path,program = program) 
        except:
            errorMsg  = "予期せぬエラーが発生しました。\n"
            import traceback
            errorMsg  +=  traceback.format_exc()


    print(errorMsg)    
    return(errorMsg)


def getErrorMsg(df,pullDown):
    # データのカラムに使う項目があるか確認
    s = _utils.columnCheck(df,colList)
    if s:
        return(s)

    # データの型の確認。
    phcVals = pullDown[phcCol].values
    ageVals = pullDown[ageCol].values
    sexVals = pullDown[sexCol].values
    valList = [phcVals, ageVals, sexVals]

    s = ''
    for col, ref in zip(colList[:-1],valList ):
        s = _utils.strTypeValCheck(df,s,col,ref)

    # 検査日のデータの確認
    # s = _utils.datetimeTypeValCheck(df,s,testDateCol)
    s = _utils.finalErrorCheck(s)
    return(s)

def diagnosticEngineering(df,pullDown,path):
    phcVals = pullDown[phcCol].dropna().values
    ageVals = pullDown[ageCol].dropna().values
    sexVals = pullDown[sexCol].dropna().values

    dfM = df.copy()
    dfM["count"] = 1 
    dfM = dataCleaning(dfM)


    regTable = _utils.basicTable(dfM, phcCol,phcVals)
    ageTable = _utils.basicTable(dfM,ageCol,ageVals)
    sexTable = _utils.basicTable(dfM,sexCol,sexVals)
    dateTable = dateTabling(dfM,testDateCol)

    regDateTable = regDateCrossTab(dfM,col1=testDateCol,col2=phcCol)
    regDateCumTable = regDateTable.cumsum()


    dir_ = _utils.getOutputDir()
    path2Save1 = dir_ + path.split("/")[-1][:-5] + f"_陽性者集計1.xlsx"
    path2Save2 = dir_ + path.split("/")[-1][:-5] + f"_陽性者集計2.xlsx"
    
    with pd.ExcelWriter(path2Save1, engine="openpyxl", mode="wa") as writer:
        #dfError = _utils.createErrorCheckDF(path)
        #dfError.to_excel(writer, sheet_name="エラー確認")

        regTable.to_excel(writer ,sheet_name="保健所")
        ageTable.to_excel(writer, sheet_name="年齢")
        sexTable.to_excel(writer, sheet_name="性別")
        dateTable.to_excel(writer, sheet_name="日付")
        regDateTable.to_excel(writer, sheet_name="日付-地域")
        regDateCumTable.to_excel(writer, sheet_name="日付-地域-累積")

    regDateAgeCrossTab(dfM,path2Save2,path,phcVals,ageVals,testDateCol,ageCol)



def dataCleaning(dfM):
    # missingは"空白" に変える
    for c in colList[:-1]:
        dfM[c]   = dfM[c].replace(np.nan,"空白")
#    dfM = dfM.replace(np.nan,"空白")

    # date conversion
    # dfM = _utils.dateTypeCheck(dfM,testDateCol)
    try:
        dfM[testDateCol] = dfM[testDateCol].dt.date
    except:
        pass

    return(dfM)


def dateTabling(df_, col):
    table = df_.groupby(by=col)["count"].sum().to_frame()
    #print(df_[col].values)
    #print(table)

    table = _utils.imputateDate(table)
    table["累積"] = table["count"].cumsum()
    return(table)



def regDateCrossTab(dfM,col1,col2):
    regDateDF = dfM.pivot_table(index = col1,columns = col2,values="count",aggfunc=np.sum)
    regDateDF = regDateDF.replace(np.nan,0)
    regDateDF = _utils.imputateDate(regDateDF)
    return(regDateDF)

def regDateAgeCrossTab(dfM,path2Save2,path,phcVals,ageVals,col1,col2): 

    with pd.ExcelWriter(path2Save2, engine="openpyxl", mode="wa") as writer:
        # dfError = _utils.createErrorCheckDF(path)
        # dfError.to_excel(writer, sheet_name="エラー確認")
        for hC in phcVals:
            cond2 = dfM[phcCol] == hC
            dfM2 = dfM[cond2]
            #print(hC)
            if dfM2.shape[0] == 0:
                continue
            regDateDF = dfM2.pivot_table(index = col1,columns = col2,values="count",aggfunc=np.sum)
            regDateDF = regDateDF.replace(np.nan,0)
            if regDateDF.shape[0] == 0:
                continue
            regDateDF = _utils.imputateDate(regDateDF)
            for c in ageVals:
                if c not in regDateDF.columns:
                    regDateDF[c] = 0
            #print(sortCol)

            #display(regDateDF)
            # save data
            regDateDF.to_excel(writer,sheet_name=hC,columns=ageVals)


if __name__ == "__main__":
    import pathList as pL
    print("スタート")
    s = main(pL.newStylePatient)
    print(s)
    print("終了")




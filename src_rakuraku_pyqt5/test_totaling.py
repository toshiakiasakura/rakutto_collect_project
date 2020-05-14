# ======================================================================
# Project Name    : rakutto_collect_project 
# File Name       : test_totaling.py
# Encoding        : utf-8
# Copyright © 2020 Toshiaki Asakura. All rights reserved.
# ======================================================================
#


import pandas as pd
import numpy as np
import datetime
import os
import sys
import _utils
import pathList as pL

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

program  = "test_totaling.py"

phcCol= '担当\n保健所' 
resultCol = '結果'
ageCol = '患者情報_年代' 
sexCol = '患者情報_性別'
testDateCol = '検査実施日'
diagnosticCol = '検査種別'
colList = [phcCol, resultCol, ageCol, sexCol, diagnosticCol]


def main(path):
    try:
        df =pd.read_excel(path,sheet_name=pL.testSheetName,encoding="cp932",header = 1)
    except:
        errorMsg = "データが読み込めませんでした。\n"
        import traceback
        errorMsg  +=  traceback.format_exc()
        print(errorMsg)
        return(errorMsg)

    errorMsg = getErrorMsg(df)
    if errorMsg == False:
        try:
            diagnosticEngineering(df,path)
            _utils.createErrorCheckFile(path,program = program)
        except:
            errorMsg  = "予期せぬエラーが発生しました。\n"
            import traceback
            errorMsg  +=  traceback.format_exc()

    print(errorMsg)    
    return(errorMsg)


def getErrorMsg(df):
    return(s)


def diagnosticEngineering(df,path):
    df = df.dropna(axis=0,how="all")

    # retrieve dataframe of diagnostic testing 
    dfM = df.copy()
    dfM = dataCleaning(dfM)


    # create crosstabulation data
    totalDF = allTotal(dfM)
    regionDF = crossTab(dfM,phcCol,resultCol)
    ageDF = crossTab(dfM,ageCol,resultCol)


    sexDF = crossTab(dfM,sexCol,resultCol)
    
    dateDF = dateCrossTab(dfM)
    dateCumDF = dateCrossTab(dfM,cum=True)

    regDateDF = regDateCrossTab(dfM)

    dir_ = _utils.getOutputDir()
    path2Save1 = dir_ + path.split("/")[-1][:-5] + "_診断検査1.xlsx"
    path2Save2 = dir_ + path.split("/")[-1][:-5] + "_診断検査2.xlsx"
    with pd.ExcelWriter(path2Save1, engine="openpyxl", mode="wa") as writer:
        #dfError = createErrorCheckDF(path)
        #dfError.to_excel(writer, sheet_name="エラー確認")

        totalDF.to_excel(writer ,sheet_name="合計")
        regionDF.to_excel(writer, sheet_name="地域")
        ageDF.to_excel(writer, sheet_name="年齢")
        sexDF.to_excel(writer, sheet_name="性別")
        dateDF.to_excel(writer, sheet_name="日付単集計")
        dateCumDF.to_excel(writer, sheet_name="日付累積")
        regDateDF.to_excel(writer, sheet_name="日付地域")

    regDateAgeCrossTab(dfM,path2Save2)

def dataCleaning(dfM):
    dfM["count"] = 1 
    # timestamp handling
    dfM[testDateCol] = _utils.convertDatetime(dfM, testDateCol) 

    # extract 診断検査
    cond = dfM[diagnosticCol]  == '診断'
    dfM  =  dfM.loc[cond]

    return(dfM)

def allTotal(dfM):
    # total
    total = dfM.groupby(resultCol)["count"].sum()
    total["総数"] = dfM.shape[0]
    total["陽性割合(%)"] = np.round(total["陽性"]/total["総数"]*100,2)
    return(total)

def crossTab(df_,col1,col2,cum = False):
    totStra = df_.pivot_table(index = col1,columns = col2,values="count",aggfunc=np.sum)
    totStra = totStra.replace(np.nan,0)
    if cum == True:
        totStra = totStra.cumsum()
    totStra["総数"] = totStra.sum(axis=1)
    totStra["陽性割合(%)"] = np.round(totStra["陽性"]/totStra["総数"]*100,2)
    
    return(totStra)

def imputateDate(totStra):
    dates = totStra.index.values
    if "空白" in dates:
        min_ = min(dates[:-1])
        max_ = max(dates[:-1])
        flag = True
    else:
        min_ = min(dates)
        max_ = max(dates)
        flag = False

    date  = min_ 
    date_sort = []
    while date <= max_:
        if date not in dates:
            totStra.loc[date] = 0
        date_sort.append(date)
        date = date + datetime.timedelta(days = 1)
        
    if flag:
        date_sort.append("空白")
    totStra = totStra.loc[date_sort]
    return(totStra)

def dateCrossTab(dfM,cum=False):
    dateDF = crossTab(dfM,testDateCol,resultCol)
    dateDF = imputateDate(dateDF)
    if cum:
        dateDF = dateDF[ ["陽性","（－）","総数"] ]
        dateDF = dateDF.cumsum()
        dateDF["陽性割合(%)"] = np.round(dateDF["陽性"] / dateDF["総数"] *100,2)
    return(dateDF)

def regDateCrossTab(dfM):
    cond = dfM[resultCol] == "陽性"
    dfMM = dfM[cond]
    col1 =  testDateCol
    col2 =  phcCol
    regDateDF = dfMM.pivot_table(index = col1,columns = col2,values="count",aggfunc=np.sum)
    regDateDF = regDateDF.replace(np.nan,0)
    regDateDF = imputateDate(regDateDF)
    return(regDateDF)

def regDateAgeCrossTab(dfM,path2Save2): 
    cond1 = dfM[resultCol] == "陽性"
    dfMM = dfM.loc[cond1]
    hCs = np.sort(dfMM[phcCol].unique())

    with pd.ExcelWriter(path2Save2, engine="openpyxl", mode="wa") as writer:
        for hC in hCs:
            cond2 = dfMM[phcCol] == hC
            dfMM2 = dfMM[cond2]
            #print(hC)
            if dfMM2.shape[0] == 0:
                continue
            col1 =  testDateCol
            col2 =  ageCol
            regDateDF = dfMM2.pivot_table(index = col1,columns = col2,values="count",aggfunc=np.sum)
            regDateDF = regDateDF.replace(np.nan,0)
            regDateDF = imputateDate(regDateDF)
            #print(sortCol)

            #display(regDateDF)
            # save data
            
            regDateDF.to_excel(writer,sheet_name=hC)

if __name__ == "__main__":
    main(pL.testData)




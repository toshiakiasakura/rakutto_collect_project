import pandas as pd
import numpy as np
import datetime
import os 
import sys
import _utils

import pathList as pL

import warnings
warnings.simplefilter('ignore')

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

program = "patient_daily_totaling.py"

posCol = "陽性確定日"
onsetCol = "発症日"
inHospCol = "入院日"
outCol = "退院日"
negSt = '陰性結果開始日'
negConf = '陰性結果確認日'
colList = [posCol,onsetCol,inHospCol,outCol,negSt,negConf]


def main(path):
    try:
        df1 = pd.read_excel(path,header=1, 
                        encodeing="cp932",
                        Sheet_name = pL.patientSheetName 
                        )
    except:
        errorMsg = "データが読み込めませんでした。\n"
        import traceback
        errorMsg  +=  traceback.format_exc()
        return(errorMsg)

    errorMsg = getErrorMsg(df1)
    if errorMsg == False:
        try:
            tableProcessing(df1,path)
            _utils.createErrorCheckFile(path, program = program) 
        except:
            errorMsg  = "予期せぬエラーが発生しました。\n"
            import traceback
            errorMsg  +=  traceback.format_exc()

    print(errorMsg)    
    return(errorMsg)


def getErrorMsg(df):
    return(False)

def tableProcessing(df1,path):
    # datetime conversion 
    for c in colList:
        try:
            df1[c] = df1[c].dt.date
        except:
            pass

    # get death date
    deathCol = "死亡日"
    status = "転帰"
    cond = df1[status] == "02_死亡"
    df1[deathCol]  = np.nan
    df1.loc[cond,deathCol] = df1.loc[cond,outCol]

    # tabling 
    df1['count'] = 1
    posi = df1[posCol].value_counts()
    posi = posi.to_frame()

    table = tablingMerge(posi, df1, onsetCol)
    table = tablingMerge(table, df1, inHospCol)

    table = tablingMerge(table, df1, negSt)
    table = tablingMerge(table, df1, negConf)

    table = tablingMerge(table, df1, outCol)
    table = tablingMerge(table, df1, deathCol)

    table = _utils.imputateDate(table)
    table = table.replace(np.nan, 0)

    table['累積陽性者数'] = table['陽性確定日'].cumsum()
    
    table['累積陰性者数'] = table['陰性結果確認日'].cumsum()

    table['累積死亡者数'] = table['死亡日'].cumsum()
    table['累積退院者数'] = table['退院日'].cumsum()
    table['累積入院者数'] = table['入院日'].cumsum()
    table['累積発症者数'] = table['発症日'].cumsum()
    table = table.rename(columns={
        '陽性確定日' : '陽性者数',
        '発症日' : '発症者数',
        '入院日' : '入院者数',
            '陰性結果開始日' : '陰性検査開始数',
            '陰性結果確認日' : '陰性者数',
        '退院日' : '退院者数', 
        '死亡日' : '死亡者数',
    })
    table['現在患者数'] = table['累積入院者数'] - table['累積退院者数'] 


    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + path.split("/")[-1][:-5] + "_table7.xlsx"
    with pd.ExcelWriter(pathOutput, engine = 'openpyxl' , mode='w') as writer: 
        table.to_excel(writer, sheet_name="日付別集計"),

def tablingMerge(table,df_,col):
    t_ = df_[col].value_counts()
    t_ = t_.to_frame()
    table = pd.concat((table,t_),join="outer")
    return(table)



if __name__ == "__main__":
    import pathList as pL
    main(pL.newStylePatient)

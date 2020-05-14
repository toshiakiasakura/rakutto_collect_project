# ======================================================================
# Project Name    : rakutto_collect_project
# File Name       : patient_info_totaling.py
# Encoding        : utf-8
# Copyright © 2020 Toshiaki Asakura. All rights reserved.
# ======================================================================
# 

import pandas as pd
import numpy as np
import re
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

program = "patient_info_totaling.py"

phc = "保健所"
statusPub = "発生状況（公表）"
physicalStatus = '身体状況（現在の症状）'

inHosp  = "入院日" 
inOrNot  = "入院の有無（入院日より）"
outOrNot = "退院の有無"


def main(path):
    try:
        df = pd.read_excel(path,
                           sheet_name=pL.patientSheetName,
                           header = 1,
                           encodeing="cp932"
                            )
        print(df.shape)
    except:
        errorMsg = "データが読み込めませんでした。\n"
        import traceback
        errorMsg  +=  traceback.format_exc()
        return(errorMsg)


    errorMsg = getErrorMsg(df)
    if errorMsg == False:
        try:
            tableProcessing(df,path)
            _utils.createErrorCheckFile(path, program = program) 
        except:
            errorMsg  = "予期せぬエラーが発生しました。\n"
            import traceback
            errorMsg  +=  traceback.format_exc()

    print(errorMsg)    
    return(errorMsg)

def getErrorMsg(df):
    return(False)



def tableProcessing(df,path):
    df = df.dropna(axis=0,how="all")
    for c in [phc,statusReal,statusPub,outOrNot,physicalStatus]:
        df[c] = df[c].replace(np.nan,'空白') 
    df["count"] =1 

    tablePub = getStatusTable(df,statusPub)
    tableReal = getStatusTable(df,statusReal)

    tablePhysical = _utils.basicTable(df,phc,physicalStatus)
    tableHosp = getHospitalTable(df)


    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + path.split("/")[-1][:-5] + f"_発生状況.xlsx"
    with pd.ExcelWriter(pathOutput , engine="openpyxl", mode="wa") as writer:
        tablePub.to_excel(writer, sheet_name="公表")
        tablePhysical.to_excel(writer, sheet_name="身体状況") 
        tableHosp.to_excel(writer,sheet_name="入院状況") 

def getStatusTable(df_,col):
    table = _utils.basicTable(df_,phc, col)
    perLis = ["01_孤発", "02_初発", "03_後発"]
    for c in perLis:
        if c not in table.columns:
            table[c] = 0 

    tablePer = table[perLis]
    tablePer = tablePer.divide(tablePer.sum(axis=1),axis=0) 
    tablePer["合計"] = tablePer.sum(axis=1) 
    tablePer = np.round(tablePer*100,2) 

    table = table.add_suffix("_(N)")
    tablePer = tablePer.add_suffix("_(%)")

    ret = pd.concat((table,tablePer),axis=1)
    return(ret)

def getHospitalTable(df_):
    df_[inHosp] = df_[inHosp].dt.date
    cond= df_[inHosp].apply(type) == type(datetime.date(2020,1,1)) 
    df_[inOrNot] = "空白"
    df_.loc[cond, inOrNot] = "有"
    tableIn  = _utils.basicTable(df_,phc,inOrNot)
    tableIn  = tableIn.add_prefix(inOrNot + "_" ) 

    tableOut = _utils.basicTable(df_,phc,outOrNot)
    tableOut = tableOut.add_prefix(outOrNot +"_")

    tableHosp = pd.concat((tableIn,tableOut),axis=1) 
#    tableHosp["現在入院患者数"] =\
#            tableHosp[inOrNot +"_有"] - tableHosp[outOrNot + "_01_有"]
    return(tableHosp)


if __name__ == "__main__":
    main(pL.newStylePatient)

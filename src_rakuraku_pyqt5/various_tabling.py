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



def daily_tabling(df,path):
    df["count"] = 1
    df = df.replace({"(.)\xa0":r"\1"},regex=True) 
    df = df.replace({"(.)\n":r"\1"},regex=True)

    posi = DailyTotal(df, '確定日（公表）', '陽性者数', '累積陽性者数')
    negStart = DailyTotal(df, '陰性結果開始日', '陰性結果開始数', '累積陰性結果開始数')
    negEnd = DailyTotal(df, '陰性結果確認日', '陰性者数', '累積陰性者数')
    inhosp = DailyTotal(df, '入院日', '入院者数', '累積入院者数')
    outhosp = DailyTotal(df, '退院日', '退院者数', '累積退院者数')
    death = DailyTotal2(df, '退院日', '身体状況（現在の症状）')
    occur = DailyTotal2(df, '確定日（公表）', '発生状況（公表）')


    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + path.split("/")[-1][:-5] + f"_日付集計.xlsx"

    with pd.ExcelWriter(pathOutput, engine = 'openpyxl' , mode='w') as writer: 
        posi.to_excel(writer, sheet_name="陽性者数"),
        negStart.to_excel(writer, sheet_name="陰性結果開始数"),
        negEnd.to_excel(writer, sheet_name="陰性者数"),
        inhosp.to_excel(writer, sheet_name="入院者数"),
        outhosp.to_excel(writer, sheet_name="退院者数"),
        death.to_excel(writer, sheet_name="身体状況別"),
        occur.to_excel(writer, sheet_name="発生状況別"),


def crossTabulation(df,path):
    hc_occur = _utils.basicTable(df, '保健所', '発生状況（公表）')
    age_hcSex = _utils.basicTable(df, '年代', ['保健所','性別'])
    hosp_bedUnhosp = _utils.basicTable(df, '入院医療機関（現在）', ['入院病床（現在）','退院の有無'])
    age_sexResult = _utils.basicTable(df, '年代', ['性別','身体状況（現在の症状）'])


    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + path.split("/")[-1][:-5] + f"_層別集計.xlsx"
    with pd.ExcelWriter(pathOutput, engine = 'openpyxl' , mode='w') as writer: 
        hc_occur.to_excel(writer, sheet_name="保健所×発生状況"),
        age_hcSex.to_excel(writer, sheet_name="年代×保健所性別"),
        hosp_bedUnhosp.to_excel(writer, sheet_name="入院医療機関×病床退院"),
        age_sexResult.to_excel(writer, sheet_name="年代×性別現在の状況"),


def DailyTotal(InputData, DateCol, ColRename, ColSumName):
    date = _utils.convertDatetime(InputData,DateCol)
    temp = date.value_counts()
    temp = temp.to_frame()
    OutputData = _utils.imputateDate(temp).replace(np.nan, 0).copy()
    OutputData[ColSumName] = OutputData[DateCol].cumsum()
    return(OutputData)


def DailyTotal2(InputData, DateCol, ColumnName):
    df_ = InputData[[DateCol, ColumnName]].copy()
    df_[DateCol] = df_[DateCol].dt.date
    df_['count'] = 1
    temp = pd.pivot_table(df_, values=['count'], index = [DateCol] , 
            columns=[ColumnName], aggfunc = np.sum, fill_value=0)
    OutputData = _utils.imputateDate(temp).copy()
    return(OutputData)










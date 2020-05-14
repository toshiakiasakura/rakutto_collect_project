# ======================================================================
# Project Name    : rakutto_collect_project
# File Name       : merge_multiple_patients.py
# Encoding        : utf-8
# Copyright © 2020 Toshiaki Asakura. All rights reserved.
# ======================================================================

import pandas as pd
import numpy as np
import datetime
import _utils
import os 
import pathList as pL

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")


def main(paths):
    dfs = []
    for path in paths:
        df =pd.read_excel(path,sheet_name=pL.patientSheetName,
                encoding="cp932",header = 1)
        dfs.append(df) 

    mergeDFs(dfs, paths)
    return(False)


def mergeDFs(dfs, paths):
    df = pd.concat(dfs,join="outer")

    path = paths[0]
    index = path.rfind("/")
    dir_ = path[ : index + 1 ]
    now = datetime.datetime.now().strftime("%Y%m%d")
    path2Save = dir_ + f"{now}_結合データ.xlsx"


    with pd.ExcelWriter(path2Save, mode="w") as writer :
        df.to_excel(writer ,index=False , 
                sheet_name=pL.patientSheetName, startrow = 1)

    col = "№"
    cond = df[col].value_counts() > 1
    if cond.sum() > 0 :
        return(f"注 : {col} には重複するデータがあります。" )





import pandas as pd
import numpy as np
import datetime
import os
import shutil
import inspect 
import sys 

if os.name == "nt":
    import locale
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")



def columnCheck(df_,colList):
    s = ""
    miss = []
    dfCols = df_.columns
    for c in colList:
        if c not in dfCols:
            miss.append(c)
    if len(miss) > 0:
        s = " ,".join(miss)
        s = '''カラム名に問題があります。
以下のカラムの名前を使うか、ファイルを確認してください。

< 足りていないカラム名 >
'''+ s
    return(s)

def strTypeValCheck(df,s,col,ref):
    '''col and ref should be "str" type.)
    '''
    miss = []
    ref = [ str(x) for x in ref]
    for d in  df[col].astype(str).dropna().unique():
        if d not in ref:
            miss.append(d)
    if len(miss) > 0 :
        refStr  = ', '.join(ref)
        missStr = ', '.join(miss)
        s += f'"{col}" は受け付けない値があります。 : [{missStr}] \n '
    return(s)

def datetimeTypeValCheck(df,s,col):
    miss = []
    flag = False
    dateType = type(datetime.datetime.now())
    timestampType = type(pd.Timestamp(2018,12,18) ) 
    NaTType = type(pd.to_datetime("a",errors="coerce"))

    for d in set(df[col].dropna()):
        if not(
               isinstance(d,timestampType) or
               isinstance(d,NaTType)
              ):
            flag = True
            if not isinstance(d, dateType):
                miss.append(str(d))
    if flag:
        missStr = ', '.join(miss)
        s += f'''"検査日"　には想定したものと違う型のデータが混じっています。
以下のデータを取り除きフォーマットを調整してください。
[{missStr}]'''
    return(s)

def finalErrorCheck(s):
    if s == '':
        return(False)
    else:
        s = '''エラーが発生しました。受け付けない値があります。
受け付ける値に関しては、リストを確認してください。

< "変数名" : 受け付けない値 >
''' + s

    return(s)


def createErrorCheckDic(path):

    def d2Str(date):
        return(date.strftime('%Y年%m月%d日_%H時%M分%S秒') )


    def ts2dt(timeStamp,str_=True):
        date = datetime.datetime.fromtimestamp(timeStamp)
        if str_ :
            date = d2Str(date)
        return(date)

    dic_ = {}
    # プログラム系
    dic_["プログラム実行日時"] = [d2Str(datetime.datetime.now())]

    # ファイル情報
    dStat  =os.stat(path)

    dic_["元データ"] = [path]
    dic_["元データ_最終アクセス日時"] = [ts2dt(dStat.st_atime)]
    dic_["元データ_最終内容更新日時"] = [ts2dt(dStat.st_mtime)]
    # 作成日時
    if os.name  == "nt":
        t = dStat.st_ctime
    elif os.name == "posix":
        t = dStat.st_birthtime
    else:
        t = np.nan
    dic_["元データ_作成日時"] = [ts2dt(t)]


    return(dic_)

def getOutputDir(create=True):
    date = datetime.datetime.now().strftime('%Y%m%d') 
    dir_ =  f"./集計データ_{date}/" 
    if not os.path.exists(dir_):
        if create:
            os.mkdir(dir_)

    return(dir_)
    
def copyOriginal(path):
    dir_ = getOutputDir()
    dirOriginal = dir_ + "元データ/" 
    if not os.path.exists(dirOriginal):
        os.mkdir(dirOriginal)

    if ".xlsx" not in path: 
        return()
    copyPath = dirOriginal + path.split("/")[-1][:-5] + "_元データ.xlsx"
    if not os.path.exists(copyPath):
        shutil.copy2(path,copyPath)


def createErrorCheckFile(path, text=None, dic_=None,program=None):
    '''output error check text, and copy the data to the directory. 
    '''
    dir_ = getOutputDir(create=False)
    if not os.path.exists(dir_):
        return()

    # check output file 
    if dic_ == None:
        dic_ = {}
    if program != None:
        dic_["プログラム名"] = [program]
    dic_ = {**dic_ , **createErrorCheckDic(path) }

    s = "##################\n"

    if text != None:
        s += s

    for k,v in dic_.items():
        s += f"{k} : {v}\n" 
    s += "\n\n"

    filePath = dir_ + "errorCheck.txt"
    with open(filePath, "a") as f :
        f.write(s) 

    # copy file 
    copyOriginal(path)


def dateTypeCheck(df_, col):
    if df_[col].dtype == "datetime64[ns]":
        df_[col] = df_[col].dt.date
#        df_[col] =  [ pd.to_datetime(x) for x in df_[col].values] 
        return(df_)


    elif  df_[col].dtype == "object":
        try:
            df_[col] = df_[col].dt.date
#            df_[col] =  [ pd.to_datetime(x) for x in df_[col].values] 
            return(df_)
        except:
            raise Exception(f"{col} is object type")
    else:
        raise Exception("unknown error occur")

def convertDatetime(df_,col):
    ser = df_[col].copy()
    if ser.dtype == "datetime64[ns]":
        ser = ser.dt.date 
    return(ser)


def imputateDate(totStra):
    dates = totStra.index.values
    if len(dates) == 0:
        return(totStra)

    min_ = min(dates)
    max_ = max(dates)

    date  = min_ 
    date_sort = []
    while date <= max_:
        date_sort.append(date)
        if date not in dates:
            totStra.loc[date] = 0
        try:
            date = date + datetime.timedelta(days=1)
        except:
            print("Error Occurs in imputateDate function") 
            return(totStra)
        
    totStra = totStra.loc[np.array(date_sort)]
    return(totStra)

def getColIndex(ws,colName,colLocNum=2):
    colIndex = False
    for  i in range(1,ws.max_column+1):
        if ws.cell(colLocNum, i)._value  == colName:
            colIndex = i
            return(colIndex)
    raise Exception(f"{colName} の名前が見つかりませんでした。")



def getColIndexDict(ws,colNames,colLocNum= 2 ) :
    dic_ = {}
    for c in colNames: 
        dic_[c] = getColIndex(ws,c,colLocNum ) 
    return(dic_) 

def getRowIndex(ws, rowName, rowLocNum):
    rowIndex = False
    for i in range(1,ws.max_row+1):
        if ws.cell(i, rowLocNum)._value  == rowName:
            rowIndex = i
            return(rowIndex)
    raise Exception(f"{rowName} の名前が見つかりませんでした。")

def getRowIndexDict(ws,rowNames,rowLocNum) :
    dic_ = {}
    for r in rowNames: 
        dic_[r] = getRowIndex(ws,r,rowLocNum) 
    return(dic_) 

def basicTable(df_,ind,col):
    df_[ind] = df_[ind].replace(np.nan,"空白") 
    df_[col] = df_[col].replace(np.nan,"空白") 

    table = df_.pivot_table(values="count",aggfunc=np.sum,
                index=ind,columns=col)
    table = table.replace(np.nan,0)
    table.loc["合計"] = table.sum(axis=0)
    table["合計"] = table.sum(axis=1)
    return(table)


# for input_form.py
class basicUtils():
    def __init__(self):
        self.nonValue = " "
        self.empty = "" 
        self.tpNumeric = "数値"
        self.tpDate    = "日付"
        self.tpDropDown= "プルタブ"  

    def convertFromStr(self, v:str, tp=None):
        if tp == self.tpNumeric :
            v = self.convert2Int(v) 
        elif tp == self.tpDate :
            v = self.convert2Date(v) 
        else:
            v = self.convert2Output(v)
        return(v) 

    def convert2Int(self, v:str):
        try:
            return(int(v)) 
        except:
            return(v) 

    def convert2Date(self, v:str):
        try:
            v = datetime.datetime.strptime(v,"%Y/%m/%d")
            return(v)
        except:
            return(v)

    def checkType(self, v:str, tp):
        flag = True
        if tp == self.tpNumeric :
            flag = self.checkInt(v) 
        elif tp == self.tpDate :
            flag = self.checkDate(v) 
        else:
            pass
        return(flag) 

    def checkInt(self, v:str):
        #print( inspect.currentframe().f_code.co_name)
        try:
            a = int(v)
            return(True)
        except:
            return(False)

    def checkDate(self, v:str):
        #print( inspect.currentframe().f_code.co_name)
        try:
            v = datetime.datetime.strptime(v,"%Y/%m/%d")
            return(True)
        except:
            return(False)

    def convert2Output(self, v:str):
        if v == self.nonValue:
            v = None
        return(v)

    def convert2Str(self, v):
        if v == None:
            v = self.nonValue 
        elif isinstance(v, datetime.datetime) :
            v = v.strftime("%Y/%m/%d") 
        else: 
            # numeric values are also converted into string. 
            v = str(v) 

        return(v) 






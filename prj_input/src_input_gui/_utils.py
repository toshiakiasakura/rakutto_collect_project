import sys
import datetime 
import inspect

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






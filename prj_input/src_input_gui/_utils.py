import sys
import datetime 

class basicUtils():
    def __init__(self):
        self.nonValue = " "
        self.empty = "" 

    def convertFromStr(self,v:str,tp=None):
        if tp == "数値" :
            v = self.convert2Int(v) 
        elif v == self.nonValue:
            v  = None
        else:
            pass
        return(v) 

    def convert2Int(self,v:str):
        try:
            return(int(v)) 
        except:
            return(v) 

    def convert2Str(self,v):
        if v == None:
            v = self.nonValue 
        elif isinstance(v, datetime.datetime) :
            v = v.strftime("%Y/%m/%d") 
        else: 
            # numeric values are also converted into string. 
            v = str(v) 

        return(v) 






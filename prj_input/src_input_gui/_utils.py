import sys
import datetime 

nonValue = " "
empty = "" 
def convertFromStr(v:str,tp=None):
    if tp == "数値" :
        v = convert2Int(v) 
    elif v == nonValue:
        v  = None
    else:
        pass
    return(v) 

def convert2Int(v:str):
    try:
        return(int(v)) 
    except:
        return(v) 

def convert2Str(v):
    if v == None:
        v = nonValue 
    elif isinstance(v, datetime.datetime) :
        v = v.strftime("%Y/%m/%d") 
    else: 
        # numeric values are also converted into string. 
        v = str(v) 

    return(v) 






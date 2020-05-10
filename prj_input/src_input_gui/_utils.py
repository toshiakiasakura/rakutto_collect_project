import sys

def checkNumeric(v,conv=False):
    if conv:
        if isinstance(v,float):
            return( str(v) ) 
        else:
            pass
    else:
        if v.isdigit(): 
            return(int(v)) 
        else:
            return(v) 

def checkStr(v):
    if v == None:
        return("")
    else:
        return(str(v)) 


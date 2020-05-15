# TO DO : 
# ・delete more data 
#   (need more deletion from data, especially for age) 

import numpy as np
import pandas as pd
import pathList as pL
import pyminizip
import _utils

def main(path ):
    try:
        df = pd.read_excel(path,
                        sheet_name=pL.patientSheetName,
                        header = 1,
                        encodeing="cp932"
                        )
    except:
        errorMsg = "データが読み込めませんでした。\n"
        import traceback
        errorMsg  +=  traceback.format_exc()
        print(errorMsg)
        return(errorMsg)


    errorMsg = getErrorMsg(df)
    if errorMsg == False:
        try:
            conversion(df,path)
            formatExcelStyle(path)
            _utils.createErrorCheckFile(path,program = program) 
        except:
            errorMsg  = "予期せぬエラーが発生しました。\n"
            import traceback
            errorMsg  +=  traceback.format_exc()
            print(errorMsg)


    print(errorMsg)    
    return(errorMsg)


def del_zip_crypt(df, path, password) :

    df = deleteItems(df,'年代：公表の可否','年代')
    df = deleteItems(df,'性別：公表の可否','性別')
    df = deleteItems(df,'居住地：公表の可否', '居住地')
    df = deleteItems(df,'居住地：公表の可否','居住地２')
    df = deleteItems(df,'職業：公表の可否', '職業分類')
    df = deleteItems(df,'職業：公表の可否', '職業２')
    df = deleteItems(df,'職業：公表の可否', '職業：備考')
    df = deleteItems(df,'発症日：公表の可否', '発症日' ) 

    for c in df.columns: 
        if "*" in c:
            del df[c] 

    # save and crypt data 
    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + path.split("/")[-1][:-5] + "_共有用.xlsx"
    sheet = pL.patientSheetName
    with pd.ExcelWriter(pathOutput, engine = 'openpyxl' , mode='wa', datetime_format='yyyy/mm/dd') as writer:
        df.to_excel(writer, startrow = 1, sheet_name = sheet, index=False)

    pathZip  = pathOutput[:-5] + ".zip"
    pyminizip.compress(pathOutput,"" , pathZip , password, 2)

def deleteItems(df_,var1,var2):
    cond = df_[var1] == "非公表"        
    df_.loc[cond,var2] = np.nan
    return(df_)


def rule(x, y):
#    try:
    v1 = np.nan
    if x == '非公表':
        v1 = np.nan
    else:
        v1 = y
    return(v1)
#    except:
#        print('exception', x)


if __name__ == "__main__":
    main(pL.newStylePatient)

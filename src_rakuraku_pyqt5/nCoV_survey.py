import openpyxl
import numpy as np
import pandas as pd
import glob
import sys
import _utils



sheet_1_name = "患者・疑似症患者臨床症状調査（添付１）"
sheet_4_name = "接触者リスト（添付3-2）"

def main(dir_):
    path2xlsx = dir_ + "/*.xlsx"
    allFilePaths = glob.glob(path2xlsx)
    extractFilePaths = [i for i in allFilePaths if '~$' not in i]
    openFilePaths = [i for i in allFilePaths if '~$' in i]
    openFileNames = [s.replace(dir_+"/", '') for s in openFilePaths]
    
    if openFileNames != []:
        print("フォルダ内に一時ファイルが存在します。ファイルが開いたままである可能性があります。確認して下さい。")
        for i in openFileNames:
            print("対象ファイル名:" + i)
        sys.exit()
    
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    
    for path in extractFilePaths:
        print(path)
        dfPre1 = pd.read_excel(path, sheet_name=sheet_1_name, encoding="cp932", header=None)
        dfPre4 = pd.read_excel(path, sheet_name=sheet_4_name, encoding="cp932", header=None)

        dfPre1 = insertOneRowCol(dfPre1)
        dfPre4 = insertOneRowCol(dfPre4)

        df1 = createMedicalHistoryDF(dfPre1,df1)
        df2 = createContactPersonsDF(dfPre1,dfPre4,df2)
    
    extractFileNames = [s.replace(dir_+"/", '') for s in extractFilePaths]
    extractFileNames.sort()
    dic_path = {"使用したファイル":extractFileNames}
    df3 = pd.DataFrame(dic_path)
    
    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + "積極的疫学調査調査票抽出データ.xlsx"
    with pd.ExcelWriter(pathOutput, engine="openpyxl", mode="w", datetime_format='yyyy/mm/dd') as writer:
        df1.to_excel(writer, sheet_name="既往歴", index=False)
        df2.to_excel(writer, sheet_name="接触者リスト", index=False)
        df3.to_excel(writer, sheet_name="使用したファイル", index=False)
        
    print("積極的疫学調査調査票抽出データ.xlsxが作成されました。")

def insertOneRowCol(df_,emp ="empty"):
    df_.index = df_.index + 1 
    df_.loc[0] = np.nan
    df_ = df_.sort_index()

    cols = df_.columns
    cols = [emp] + list(cols)
    df_[emp] = np.nan 
    df_ = df_[cols]
    return(df_)


def createMedicalHistoryDF(dfPre1,df):

    #患者情報
    patient_id = "患者ID"
    patient_name = "患者氏名"

    patient_id_v = dfPre1.iloc[4,38]
    patient_name_v = dfPre1.iloc[19,9]

    #元データの疾患名, 列位置
    preg ='妊娠'
    smok = '喫煙'
    diab = '糖尿病'
    resp_dis = '呼吸器疾患（喘息・COPD・その他）'
    rena_dis = '腎疾患'
    live_dis = '肝疾患'
    hear_dis = '心疾患'
    nerv_dis = '神経筋疾患'
    bloo_dis = '血液疾患（貧血等）'
    immu = '免疫不全（HIV、免疫抑制剤使用含む）'
    canc = '悪性腫瘍（がん）'

    mhcp = medical_history_column_position = 4

    mark='■'
    no_mark="□"
    k1cp = key_1_column_position = 22
    k2cp = key_2_column_position = 25

    #疾患名出力表のカラム名変更
    preg_out ='妊娠'
    smok_out = '喫煙'
    diab_out = '糖尿病'
    resp_dis_out = '呼吸器疾患'
    rena_dis_out = '腎疾患'
    live_dis_out = '肝疾患'
    hear_dis_out = '心疾患'
    nerv_dis_out = '神経筋疾患'
    bloo_dis_out = '血液疾患'
    immu_out = '免疫不全'
    canc_out = '悪性腫瘍'

    #詳細情報1
    preg_week = '妊娠週数'
    smok_start_age = '喫煙：歳から'
    smok_per_day = '喫煙：本／日'
    dialysis = '（腎透析）'

    pwcp = preg_week_column_position = 31
    ssacp = smok_start_age_column_position = 29
    spdcp = smok_per_day_column_position = 35
    dk1cp = dialysis_key_1_column_position = 36
    dk2cp = dialysis_key_2_column_position = 40

    #詳細情報2
    resp_dis_detail = "呼吸器疾患詳細"
    live_dis_detail = "肝疾患詳細"
    hear_dis_detail = "心疾患詳細"
    nerv_dis_detail = "神経筋疾患詳細"
    bloo_dis_detail = "血液疾患詳細"
    immu_detail = "免疫不全詳細"
    canc_detail = "悪性腫瘍詳細"

    mhdcp = medical_history_column_position =33

    #その他疾患
    other_dis = "その他疾患"
    odcp = other_dis_column_position = 8

    #出力表のカラム順番変更
    out_order_list = [
        preg,
        preg_week,
        smok,
        smok_start_age,
        smok_per_day,
        diab,
        resp_dis,
        rena_dis,
        dialysis,
        live_dis,
        hear_dis,
        nerv_dis,
        bloo_dis,
        immu,
        canc,
        other_dis,
    ]

    out_list = [
        preg_out,
        preg_week,
        smok_out,
        smok_start_age,
        smok_per_day,
        diab_out,
        resp_dis_out,
        rena_dis_out,
        dialysis,
        live_dis_out,
        hear_dis_out,
        nerv_dis_out,
        bloo_dis_out,
        immu_out,
        canc_out,
        other_dis
    ]
    
    
    
    col_1 =[
        preg,
        smok,
        diab,
        resp_dis,
        rena_dis,
        live_dis,
        hear_dis,
        nerv_dis,
        bloo_dis,
        immu,
        canc
    ]

    dic_1 = getRowIndexDict(dfPre1,col_1,mhcp)

    yes_no_l = []
    for i in dic_1.values():
        v1 = c_value(dfPre1,i,k1cp)
        v2 = c_value(dfPre1,i,k2cp)
        if (v1 == mark) & (v2 == no_mark):
            x = c_value(dfPre1,i,k1cp+1)
        elif (v1 == no_mark) & (v2 == mark):
            x = c_value(dfPre1,i,k2cp+1)
        elif (v1 == no_mark) & (v2 == no_mark):
            x = "記入なし"
        else:
            x = "error"
        yes_no_l.append(x)

    dic_1_yn = {}
    for k,v in zip(col_1,yes_no_l):
        dic_1_yn[k]=v

    dic_2 = {
        preg_week:[c_value(dfPre1,dic_1[preg],pwcp)],
        smok_start_age:[c_value(dfPre1,dic_1[smok],ssacp)],
        smok_per_day:[c_value(dfPre1,dic_1[smok],spdcp)],
    }

    s1=c_value(dfPre1,dic_1[rena_dis],dk1cp)
    s2=c_value(dfPre1,dic_1[rena_dis],dk2cp)

    if (dic_1_yn[rena_dis]==c_value(dfPre1,dic_1[rena_dis],k1cp+1)) & (s1==no_mark) & (s2==no_mark): 
        x = "腎疾患なし"
    elif (dic_1_yn[rena_dis]==c_value(dfPre1,dic_1[rena_dis],k2cp+1)) & (s1==mark) & (s2==no_mark): 
        x = c_value(dfPre1,dic_1[rena_dis],dk1cp+1)
    elif (dic_1_yn[rena_dis]==c_value(dfPre1,dic_1[rena_dis],k2cp+1)) & (s1==no_mark) & (s2==mark): 
        x = c_value(dfPre1,dic_1[rena_dis],dk2cp+1)
    elif (dic_1_yn[rena_dis]==c_value(dfPre1,dic_1[rena_dis],k2cp+1)) & (s1==no_mark) & (s2==no_mark): 
        x = "透析記入なし"
    else:
        x = "error"

    dic_3 = {
        dialysis:x
    }

    dic_4 = {
        resp_dis_detail:[c_value(dfPre1,dic_1[resp_dis],mhdcp)],
        live_dis_detail:[c_value(dfPre1,dic_1[live_dis],mhdcp)],
        hear_dis_detail:[c_value(dfPre1,dic_1[hear_dis],mhdcp)],
        nerv_dis_detail:[c_value(dfPre1,dic_1[nerv_dis],mhdcp)],
        bloo_dis_detail:[c_value(dfPre1,dic_1[bloo_dis],mhdcp)],
        immu_detail:[c_value(dfPre1,dic_1[immu],mhdcp)],
        canc_detail:[c_value(dfPre1,dic_1[canc],mhdcp)],
    }

    dic_5 = {
        other_dis:[c_value(dfPre1,max(dic_1.values())+1,odcp)]
    }

    dic_merge = dic_1_yn
    dic_merge.update(dic_2)
    dic_merge.update(dic_3)
    dic_merge.update(dic_5)

    collect_data_list = []
    for i in out_order_list:
        collect_data_list.append(dic_merge[i])

    dic_all = {}
    for k,v in zip(out_list,collect_data_list):
        dic_all[k]=v

    dic_all.update(dic_4)

    dic_patient = {
        patient_id:patient_id_v,
        patient_name:patient_name_v,
    }

    dic_patient.update(dic_all)
    df_patient = pd.DataFrame(dic_patient)
    df = pd.concat([df, df_patient])
    
    return(df)

def createContactPersonsDF(dfPre1,dfPre4,df):


    #患者情報
    patient_id = "患者ID"
    patient_name = "患者氏名"

    patient_id_v = dfPre1.iloc[4,38]
    patient_name_v = dfPre1.iloc[19,9]

    #元データのカラム名、カラム位置、マーク文字、マークサーチ範囲
    ct_num="接触者"
    name="氏名"
    yomi="よみがな"
    rel="続柄"
    age="年齢"
    sex="性別"
    ct_time="患者との"
    ud_dis="基礎"
    onset="観察期間内"
    adr="連絡先（電話番号、"
    other="備考（接触状況等）"

    cln=5

    mark='■'
    no_mark="□"
    cvr=3

    col_1=[ct_num,name,yomi,rel,age,adr,other]
    col_2=[sex, ud_dis, onset]
    col_3 = [ct_time]

    #出力表のカラム名変更
    ct_num_out="接触者番号"
    name_out="氏名"
    yomi_out="よみがな"
    rel_out="続柄（関係）"
    age_out="年齢"
    sex_out="性別"
    ct_time_out="患者との最終接触日"
    ud_dis_out="基礎疾患"
    onset_out="観察期間内の発症"
    adr_out="連絡先（電話番号、メールアドレス等）"
    other_out="備考（接触状況等）"

    #出力表のカラム順番変更
    out_order_list = [
        ct_num,
        name,
        yomi,
        rel,
        age,
        sex,
        ct_time,
        ud_dis,
        onset,
        adr,
        other,
    ]

    out_list = [
        ct_num_out,
        name_out,
        yomi_out,
        rel_out,
        age_out,
        sex_out,
        ct_time_out,
        ud_dis_out,
        onset_out,
        adr_out,
        other_out,
    ]

    dic_1=getColIndexDict(dfPre4,col_1,cln)

    name_l=[]
    for i in range(cln+2,dfPre4.shape[0]-1):
        x= c_value( dfPre4, i, dic_1[name])
        
        if x!=x:
            break
        name_l.append(x)
    col_len=len(name_l)

    dic_l_1 = {}
    for k,v in dic_1.items():
        l = list()
        for i in range (cln+2,col_len+cln+2):
            l.append(c_value( dfPre4,i ,v))
        x = {k:l}
        dic_l_1.update(x)

    dic_2=getColIndexDict(dfPre4,col_2,cln)


    dic_l_2 = {}
    for k,v in dic_2.items():
        l = list()
        for i in range (cln+2,col_len+cln+2):
            v1 = c_value( dfPre4,i, v)
            v2 = getItems_SeeSameRowItems(dfPre4,i,v+1,cvr,mark) or getItems_SeeSameRowItems(dfPre4,i,v+1,cvr,no_mark)
            if (v1 == mark) & (v2 == no_mark):
                x = c_value( dfPre4,i, v+1)
            elif (v1 == no_mark) & (v2 == mark):
                n = seeSameRowItems(dfPre4,i,v+1,cvr).index(mark)
                x = c_value( dfPre4, i, v+n+2)
            elif (v1 == no_mark) & (v2 == no_mark):
                x = "入力なし"
            else:
                x = "error"
            l.append(x)
        x = {k:l}
        dic_l_2.update(x)

    dic_3 = getColIndexDict(dfPre4,col_3,cln)

    dic_l_3 = {}
    for k,v in dic_3.items():
        l = list()
        for i in range (cln+2,col_len+cln+2):
            a = c_value(dfPre4,i, v)
            b = c_value(dfPre4,i, v+3)
            c = c_value(dfPre4,i, v+6)
            date = convertStr2Date(a,b,c)
            l.append(date)

        x = {k:l}
        dic_l_3.update(x)

    dic_merge = dic_l_1
    dic_merge.update(dic_l_2)
    dic_merge.update(dic_l_3)

    collect_data_list = []
    for i in out_order_list:
        collect_data_list.append(dic_merge[i])

    dic_all = {}
    for k,v in zip(out_list,collect_data_list):
        dic_all[k]=v

    patient_id_l = []
    for i in range (1,col_len+1):
        patient_id_l.append(patient_id_v)

    patient_name_l = []
    for i in range (1,col_len+1):
        patient_name_l.append(patient_name_v)

    dic_patient = {
        patient_id:patient_id_l,
        patient_name:patient_name_l,
    }

    dic_patient.update(dic_all)
    df_patient = pd.DataFrame(dic_patient)
    df = pd.concat([df, df_patient])

    return(df)


def convertStr2Date(y,m,d):
    y = convert2Str(y)
    m = convert2Str(m)
    d = convert2Str(d) 
    if y == None or m == None or d == None:
        return(np.nan)

    if "R" in y:
        y = 2018 +  int(y[1:]) 
        y = str(y)
    if len(y) == 1 :
        y = 2018 + int(y)
        y = str(y)

    date = f"{y}/{m}/{d}"
    date = pd.to_datetime(date)
    return(date)

def convert2Str(v):
    if isinstance(v, float):
        if np.isnan(v):
            return(None)
        v = int(v)

    v = str(v) 
    return(v) 

def seeSameRowItems(df_,row_n,start_col_n,cover_range):
    l = []
    for i in range(1,cover_range+1):
        l.append( c_value(df_ ,row_n, start_col_n+i-1) )
    return l

def getItems_SeeSameRowItems(df_ ,row_n,start_col_n,cover_range,item):
    x = seeSameRowItems(df_ ,row_n,start_col_n,cover_range)
    if (item in x):
        return item
    

def c_value(df_,r,c):
    return df_.iloc[r,c]


def getColIndex(df_,colName,colLocNum=2):
    colIndex = False
    for  i in range(1,df_.shape[1]):
        if df_.iloc[colLocNum, i]== colName:
            colIndex = i
            return(colIndex)
    raise Exception(f"{colName} の名前が見つかりませんでした。")



def getColIndexDict(df_,colNames,colLocNum= 2 ) :
    dic_ = {}
    for c in colNames:
        dic_[c] = getColIndex(df_,c,colLocNum )
    return(dic_)

def getRowIndex(df_, rowName, rowLocNum):
    rowIndex = False
    for i in range(1,df_.shape[0]):
        if df_.iloc[i, rowLocNum] == rowName:
            rowIndex = i
            return(rowIndex)
    raise Exception(f"{rowName} の名前が見つかりませんでした。")

def getRowIndexDict(df_,rowNames,rowLocNum) :
    dic_ = {}
    for r in rowNames:
        dic_[r] = getRowIndex(df_,r,rowLocNum)
    return(dic_)

if __name__ == "__main__":
    dir_ = "../dt_20200518/rakuraku_format/"
    main(dir_)

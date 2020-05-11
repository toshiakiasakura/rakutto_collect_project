from openpyxl import Workbook
from openpyxl import load_workbook

path = "./test_data.xlsx"
shName1 = "患者情報入力シート"
shName2 = "患者プルタブシート" 

def main():
    wb = load_workbook(path)
    wbBase = load_workbook(path)
    ws1 = wb[shName1]
    wsBase = wbBase[shName1] 

    ws1.cell(1,1).value = "changed"
    print(ws1.cell(1,1).value, wsBase.cell(1,1).value)


if __name__ == "__main__":
    main()

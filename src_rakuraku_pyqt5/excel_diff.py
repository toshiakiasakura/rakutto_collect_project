import pandas as pd
import numpy as np
from datetime import datetime

import _utils


def main(old, new):
    mod_df, add_df, rem_df = excel_diff(old, new)

    # export to an excel file
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_ = _utils.getOutputDir()
    pathOutput = dir_ + f'新旧比較_{now}.xlsx' 

    with pd.ExcelWriter(pathOutput, engine='openpyxl', mode='w',
                        datetime_format='yyyy/mm/dd') as writer:
        mod_df.to_excel(writer, sheet_name='既存データへの変更', index=False, header=False)
        add_df.to_excel(writer, sheet_name='新規追加データ', index=False, header=False)
        rem_df.to_excel(writer, sheet_name='削除されたデータ', index=False, header=False)




def excel_diff(old, new):
# gets old and new dataframes
# returns dataframes of modified data, newly added records, and removed records

    # replace nan with string ('na_str')
    nan_str = 'na_str'
    old = old.fillna(nan_str)
    new = new.fillna(nan_str)

    # take each record from new file and compare it with the older one
    column_list = list(new.columns)

    # list of modified data with header
    mod_list = [['', '新行番号', '新列番号', '№', '項目名', '変更前の値', '変更後の値']]
    mod_row_id = 0
    # list of newly added data with header
    add_list = [['', '新行番号', *column_list]]
    add_row_id = 0

    for row_num, new_rec in new.iterrows():
        # process only if the new_rec contains any value but nan_str
        # (i.e. ignore empty rows)
        if not any(new_rec!=nan_str):
            continue

        no = new_rec['№']
        old_rec = old[old['№']==no]

        if len(old_rec) == 1: # if a corresponding record is found
            old_rec = old_rec.iloc[0] # convert old_rec into Series

            # compare each value with the older record

            eq = new_rec.eq(old_rec) # Series
            if not eq.all(): # if there has been an update
                old_vals = old_rec[~eq] # Series
                new_vals = new_rec[~eq] # Series

                for i, change in enumerate(zip(new_vals.index.values, new_vals)):
                    col_num = column_list.index(change[0]) + 1
                    diff = [mod_row_id, row_num + 3, col_num, no,
                            change[0], old_vals[i], change[1]]

                    # replace nan_str with ''
                    diff = ['' if s==nan_str else s for s in diff]

                    # add new row to the list for output
                    mod_list.append(diff)
                    mod_row_id += 1

        elif len(old_rec) > 1: # if multiple corresponding records are found
            # I don't know how to handle this situation (ishii)
            print('error! duplicated record!')

        else:
            # add new_rec to the new record list
            add = [add_row_id, row_num + 3, *list(new_rec)]
            # replace nan_str with ''
            add = ['' if s==nan_str else s for s in add]
            add_list.append(add)
            add_row_id += 1

    # extract removed records
    no_in_old = old['№'].unique().tolist() # no.s contained in the old file
    if nan_str in no_in_old:
        no_in_old.remove(nan_str) # remove nan_str

    no_in_new = new['№'].unique().tolist() # no.s contained in the new file
    if nan_str in no_in_old:
        no_in_new.remove(nan_str) # remove nan_str

    rem_list = [['', '旧行番号', *column_list]]
    rem_row_id = 0

    for no in no_in_old:
        if not no in no_in_new: # if there is no corresponding record in the new
            cond = old['№'] == no
            row_num = old[cond].index[0] + 3
            rem_rec = list(old[cond].iloc[0])
            rem = [rem_row_id, row_num, *rem_rec]
            # replace nan_str with ''
            rem = ['' if s==nan_str else s for s in rem]
            rem_list.append(rem)
            rem_row_id += 1

    # convert lists to dataframe
    mod_df = pd.DataFrame(mod_list)
    add_df = pd.DataFrame(add_list)
    rem_df = pd.DataFrame(rem_list)

    return mod_df, add_df, rem_df


if __name__ == "__main__":
    path1 = '../dt_test/excel_diff/patient_example_v05.xlsx'
    path2 = '../dt_test/excel_diff/patient_example_v05_modified-sample.xlsx'
    old = pd.read_excel(path1, encoding='cp932', header=1)
    new = pd.read_excel(path2, encoding='cp932', header=1)
    main(old, new)

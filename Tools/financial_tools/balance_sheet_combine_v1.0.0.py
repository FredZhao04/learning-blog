# !/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter.filedialog import askdirectory
import pandas as pd
import os
'''
  批量合并资产负债表
'''
root = tk.Tk()
root.title("批量合并资产负债表工具-V1.0.0")
root.geometry('800x400')


type_Label = tk.Label(root, text="合并资产负债表", width=20, heigh=3)
var1 = tk.StringVar()
InfoListbox = tk.Listbox(root, listvar=var1, width=80, heigh=16)

pd.set_option('display.max_columns', None)   # 显示完整的列
pd.set_option('display.max_rows', None)  # 显示完整的行
pd.set_option('display.expand_frame_repr', False)  # 设置不折叠数据

def delete_space(item):
    if isinstance(item, str):
        return item.strip()

def read_excel(file_path):
    try:
        data = pd.read_excel(file_path, sheet_name="资产负债表")

        item_list = []
        value_list = []
        for i in range(2, data.shape[0]):
            item_list.append(delete_space(data.iloc[i, 0]))
            value_list.append(data.iloc[i, 1])

        for i in range(2, data.shape[0]):
            item_list.append(delete_space(data.iloc[i, 3]))
            value_list.append(data.iloc[i, 4])
        df = pd.DataFrame({"item":item_list, "value":value_list})
        df = df[df['item'].notnull()]
        df = df.fillna(0)

        return df
    except:
        return None


def select_path():
    path_ = askdirectory()
    return path_


def start():
    df_all = pd.DataFrame()
    path = select_path()
    files = os.listdir(path)
    length = len(files)
    n = 0
    for file in files:
        n += 1
        file_path = os.path.join(path, file)
        df_tmp = read_excel(file_path)
        if df_tmp is not None:
            df_tmp.set_index(['item'], inplace=True)
            if df_all.empty:
                df_all = df_tmp
            else:
                df_all = pd.merge(df_all, df_tmp, on="item")
        if int(n%(int(length/10))) == 0:
            InfoListbox.insert(tk.END, "已处理{}的文件".format(n))
            InfoListbox.update()
    save_path = os.path.join(path, "合并资产负债表.csv")
    df_all.to_csv(save_path, header=False, index=True, mode='w')
    InfoListbox.insert(tk.END, "合并资产负债表流程已结束！！！")
    InfoListbox.update()


check = tk.Button(root, text="选择保存路径并开始", width=20, fg="black", command=start)

type_Label.grid(row=0, column=0)

check.grid(row=0, column=2, padx=20)

InfoListbox.grid(row=1, columnspan=3, pady=15, padx=10)

root.mainloop()

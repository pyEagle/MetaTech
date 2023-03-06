# -*- coding:utf-8 -*-

import pandas as pd


def multi_excel_sum(xlsx_files, drop_keys, out_file):
    data = pd.read_excel(xlsx_files[0])
    key_list = data.columns.tolist()
    key_list.remove(drop_keys)

    suffix = ['_x', '_y']
    for x in xlsx_files[1:]:
        temp = pd.read_excel(x)
        data = pd.merge(data, temp, how='outer', on=[drop_keys], suffixes=suffix)
        data.fillna(0, inplace=True)

        for key in key_list:
            data[key] = data[key+'_x']+data[key+'_y']

        drop_labels = [c for c in data.columns if c.endswith('x') or c.endswith('y')]
        data.drop(labels=drop_labels, axis=1, inplace=True)

    data.to_excel(out_file, index=False)


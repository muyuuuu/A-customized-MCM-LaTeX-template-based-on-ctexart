import numpy as np
import pandas as pd
from collections import Counter

def step1(df):
    keep_typeOfData_list = list('PDRX')  
    df_rest = [df.Year]
    for i in range(1, len(df.columns)):
        column = df.iloc[:, i]
        if column.name[-1] in keep_typeOfData_list:
            df_rest.append(column)

    df_rest = pd.concat(df_rest, axis=1)
    return df_rest

def step2(df, threshold=.7):
    df_rest = [df.Year]
    for i in range(1, len(df.columns)):
        column = df.iloc[:, i]
        if sum(column == 0) < threshold:  # 阈值判断
            df_rest.append(column)
    df_rest = pd.concat(df_rest, axis=1)
    return df_rest

def step3(df, df_raw):
    renewable = ['BM', 'EL', 'EM', 'EN', 'ES', 'GE', 'HY', 'NU',
                 'RE', 'RO', 'SO', 'WD', 'WS', 'WW', 'WY']
    df_add = []
    for i in range(1, len(df_raw.columns)):
        column = df_raw.iloc[:, i]
        name = column.name
        if name[:2] in renewable and name not in df.columns:
            df_add.append(column)
    df_add = pd.concat(df_add, axis=1)
    df = pd.concat([df, df_add], axis=1)
    return df

if __name__ == "__main__":
    df_AZ = pd.read_excel('./data/data_set.xlsx', sheet_name='AZ')
    df_CA = pd.read_excel('./data/data_set.xlsx', sheet_name='CA')
    df_NM = pd.read_excel('./data/data_set.xlsx', sheet_name='NM')
    df_TX = pd.read_excel('./data/data_set.xlsx', sheet_name='TX')
    df_rest_AZ = step3(step2(step1(df_AZ)), df_AZ)
    df_rest_CA = step3(step2(step1(df_CA)), df_CA)
    df_rest_NM = step3(step2(step1(df_NM)), df_NM)
    df_rest_TX = step3(step2(step1(df_TX)), df_TX)

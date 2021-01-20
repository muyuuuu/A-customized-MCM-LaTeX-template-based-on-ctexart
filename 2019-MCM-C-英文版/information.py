import numpy as np
import pandas as pd
import os

def calc_ent(x):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    return ent

def calc_condition_ent(x, y):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        sub_y = y[x == x_value]
        temp_ent = calc_ent(sub_y)
        ent += (float(sub_y.shape[0]) / y.shape[0]) * temp_ent

    return ent

def calc_info_gain(x, y):
    base_ent = calc_ent(y)
    condition_ent = calc_condition_ent(x, y)
    ent_grap = base_ent - condition_ent

    return ent_grap

years = [i for i in range(2010, 2017)]

df_opioid_all = pd.read_excel('data/MCM_NFLIS_Data.xlsx')
df_opioid_all = df_opioid_all[['YYYY', 'FIPS_Combined', 'DrugReports']]
df_opioid_list = []
for year in years:
    df = df_opioid_all.loc[df_opioid_all['YYYY'] == year]
    df.drop('YYYY', axis=1, inplace=True)
    df_opioid_list.append(df.groupby(['FIPS_Combined']).sum())

base_path = 'data/ACS_{YY}_5YR_DP02/ACS_{YY}_5YR_DP02_with_ann.csv'
filepaths = [base_path.format(YY=i) for i in range(10, 17)]
df_census_list = []
for filepath in filepaths:
    df = pd.read_csv(filepath, skiprows=[1], index_col='GEO.id2',
                     na_values=['**', '-', '***', '*****', 'N', '(X)'])
    df.drop(['GEO.id', 'GEO.display-label'], axis=1, inplace=True)
    df.sort_index(axis=1, inplace=True)
    df_census_list.append(df)
    
df_attrs = pd.read_excel('data/socio-economic.xlsx')
attr_dict = dict(zip(df_attrs['code'], df_attrs['chinese']))

s_list = []

attr_codes = set(df_census_list[-1].columns).union(set(df_census_list[0].columns))
s_list.append(pd.Series([attr_dict.get(attr_code) for attr_code in attr_codes],
                        index=attr_codes))

for i in range(7):
    df_opioid = df_opioid_list[i]
    df_census = df_census_list[i]
    
    info_gains = []
    for attr_code in df_census:
        df_temp = pd.DataFrame()
        df_temp['attr'] = df_census[attr_code]
        df_temp['opioid'] = df_opioid['DrugReports']
        a = df_temp.values
        attr_array = a[:, 0].ravel()
        opioid_array = a[:, 1].ravel()
        attr_array = np.nan_to_num(attr_array)
        opioid_array = np.nan_to_num(opioid_array)
        info_gain = calc_info_gain(opioid_array, attr_array)
        info_gains.append(info_gain)
    
    s_list.append(pd.Series(info_gains, index=df_census.columns))

result_col_names = ['attr_desc'] + years
df_result = pd.DataFrame({str(result_col_names[i]): s_list[i] for i in range(8)})
df_result = df_result.iloc[:190]
df_result['average'] = df_result.mean(axis=1, numeric_only=True)

df_result.to_excel('data/result.xlsx')
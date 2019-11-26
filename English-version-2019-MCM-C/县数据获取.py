# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('data/heroin.xlsx')
state = 'WV'
df = df[df.State == state]
df_new = df.groupby(['YYYY', 'FIPS_Combined']).sum().DrugReports

years = df_new.index.levels[0]
states = df_new.index.levels[1]
data = []
for year in years:
    temp = []
    for state in states:
        res = 0
        if state in df_new[year]:
            res = df_new[year][state]
        temp.append(res)
    data.append(temp)


df_new = pd.DataFrame(data, index=years, columns=states)

df_new.to_excel('data/state_heroin.xlsx')

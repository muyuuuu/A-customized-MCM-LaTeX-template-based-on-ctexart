# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import pylab as pl
import seaborn as sns


def predict(m):
    t = t_2017.copy()
    t_predict = []
    years = 10
    for _ in range(years):
        t = np.dot(t, m)
        t_predict.append(t[0])

    index = [2018+i for i in range(years)]
    t_predict = pd.DataFrame(t_predict, index=index, columns=df.columns)

    return t_predict


def getMatrix(df, year_before=2010, year_after=2011):
    status_before = df[df.index == year_before].values
    status_after = df[df.index == year_after].values
    status_pinv = np.linalg.pinv(status_before)

    # dot
    transfer_matrix = np.dot(status_pinv, status_after)

    return transfer_matrix


df = pd.read_csv('data/FIPS_groupby_year_state.csv',
                 engine='python', index_col=0)
m = getMatrix(df, 2016, 2017)
t_2017 = df[df.index == 2017].values

data = df.iloc[:, 1]
p = predict(m).iloc[:, 1]
data = pd.concat([data, p])


m_ = m**1.1


p = predict(m_).iloc[:, 1]
p = np.append([119349], p)
p = pd.Series(p, index=list(range(2017, 2027+1)))
data = pd.concat([data, p], axis=1)
data.columns = ['normal', 'decrease']

# plot
pl.style.use('ggplot')
pl.figure(figsize=(14, 8))
ax = pl.gca()
ax.yaxis.major.formatter.set_powerlimits((0, 0))
sns.lineplot(data=data)
pl.axvline(x=2017, linestyle=':')
pl.xticks(list(range(2010, 2027+1)), list(range(2010, 2027+1)),
          rotation=20, fontsize=12)
pl.xlabel('Year', fontsize=15)
pl.yticks(fontsize=12)
pl.legend(fontsize=15)
pl.savefig('assets/OH_predict.png', dpi=500)
pl.show()

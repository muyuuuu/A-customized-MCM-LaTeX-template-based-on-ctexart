# -*- coding: utf-8 -*-
import pandas as pd

state_labels = [21, 39, 42, 51, 54]
missing_lables = ['**', '-', '***', '*****', 'N', '(X)']


def concat_county(df):
    # drop nan data
    for missing_label in missing_lables:
        df.replace(missing_label, 0, inplace=True)

    # concat the same state data
    df_state = df['GEO.id2'].apply(lambda x: int(str(x)[:2]))
    df_state.name = 'state'
    df.drop(columns='GEO.id2', inplace=True)
    df.drop(columns='GEO.id', inplace=True)
    df.drop(columns='GEO.display-label', inplace=True)
    df = df.astype(float)

    df = pd.concat([df_state, df], axis=1)
    df_group = df.groupby('state').sum()

    return df_group


if __name__ == "__main__":
    df_state = [[] for i in range(len(state_labels))]
    for year in range(10, 16+1):
        fname = 'data/ASC/ACS_{}_5YR_DP02_with_ann.csv'.format(year)
        df = pd.read_csv(fname, encoding='utf-8')
        df.drop(0, inplace=True)
        df = concat_county(df)
        for ind, state_label in enumerate(state_labels):
            temp = df[df.index == state_label]
            df_state[ind].append(temp)

    years = list(range(2010, 2016+1))
    for ind, state_label in enumerate(state_labels):
        df_state[ind] = pd.concat(df_state[ind])
        df_state[ind].index = years

    writer = pd.ExcelWriter('data/socio-economic_groupby_year_state.xlsx')
    for i, state in enumerate(state_labels):
        df_state[i].to_excel(writer, sheet_name=str(state))
    writer.save()

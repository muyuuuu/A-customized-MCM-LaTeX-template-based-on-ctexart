# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_excel(
    'data/countys_nonheroin_mean_transport_matrix.xlsx', index_col=0)

plt.figure(figsize=(16, 16))
plt.gca().set_aspect(1)
sns.heatmap(df.values)
plt.xticks(range(len(df)), df.index, rotation=90,
           horizontalalignment="left")
plt.yticks(range(len(df)), df.index, rotation=360,
           horizontalalignment="right")

# plt.gca().xaxis.tick_top()
plt.title('WV Countys Narcotic Analgesics Transition Matrix', fontsize=25)
plt.savefig('assets/county_nonheroin_transition_matrix.png', dpi=500)
# plt.show()

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df_one = pd.read_excel(
    'data/state_heroin_mean_transport_matrix.xlsx', index_col=0)
df_another = pd.read_excel(
    'data/state_nonheroin_mean_transport_matrix.xlsx', index_col=0)

labels = ['KY', 'OH', 'PA', 'VA', 'WV']

plt.style.use('ggplot')
plt.figure(figsize=(12, 6))
plt.gca().set_aspect(1)

plt.subplot(121)
plt.imshow(df_one)
plt.xticks(range(len(labels)), labels, fontsize=13)
plt.yticks(range(len(labels)), labels, rotation=360)
plt.title('States Heroin Transition Matrix', fontsize=20)

plt.subplot(122)
plt.imshow(df_another)
plt.xticks(range(len(labels)), labels, fontsize=13)
plt.yticks(range(len(labels)), labels, rotation=360, fontsize=13)
plt.title('States Narcotic Analgesics Transition Matrix', fontsize=20)
plt.tight_layout()
plt.subplots_adjust(bottom=0.1, right=0.9, top=0.9)
cax = plt.axes([0.92, 0.1, 0.02, 0.8])
plt.colorbar(cax=cax)

plt.savefig('assets/state_drug_transition_matrix.png', dpi=500)
# plt.show()

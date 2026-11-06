import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('path', delimiter=';')
df.set_index(['nametags', 'uso_cluster'],inplace=True)
df['iaccs'] = df['iaccs'].agg(lambda x: 100 - x)
df.fillna(0,inplace=True)
fig, ax = plt.subplots()
dfRenamed= df.copy().rename(columns = {'iaccs': 'all participants'})
"""
ax.boxplot(scatterPrepY.values, notch=False, vert=True, autorange=True, patch_artist = True,showbox=False,
                  medianprops={"color": "gainsboro", "linewidth": 0.5},
                whiskerprops={"color": "gainsboro", "linewidth": .5},
                capprops={"color": "gainsboro", "linewidth": .5})
"""

# plot all
df['iaccs'] = df['iaccs'].agg(lambda x: 100 - x)
scatterPrepY = df.groupby('nametags', dropna=False)['iaccs'].mean()
scatterPrepX = ['all participants' for i in range(scatterPrepY.__len__())]
ax.scatter(scatterPrepX,scatterPrepY, c="gray", label="participants")
ax.errorbar(['all participants'], df['iaccs'].mean(), yerr= df['iaccs'].std(), fmt='k_', markersize= 30, ecolor='gainsboro', label='Mean')
refline = np.array([[abs(0.975-df.xs('J2',level='nametags')['iaccs'].mean())],[0]])
ax.errorbar(['all participants'], 1, yerr=refline, fmt='b_', markersize= 30, ecolor='lightsteelblue', label='Reference', uplims=True)
ax.set_ylim(0,1.1)
ax.set_ylabel('Interaural cross correlation')
ax.legend()

# clusterwise plot
df = pd.read_csv('path', delimiter=';')
df.fillna(0,inplace=True)
df['iaccs'] = df['iaccs'].agg(lambda x: 100 - x)

for participant in df.index.get_level_values('nametags').drop_duplicates().values:
    if df.xs(participant, level='nametags').__len__() < 4:
        continue
    ax.plot(['a','b','c','d'], df.xs(participant, level='nametags')['iaccs'].values, color='gainsboro',marker='o',linestyle=':')

for cluster, category in zip(df.index.get_level_values('uso_cluster').drop_duplicates().values, ['a', 'b', 'c', 'd']):
    dfcluster = df.xs(cluster, level='uso_cluster')
    ax.errorbar(category, dfcluster['iaccs'].mean(), yerr=dfcluster['iaccs'].std(), fmt='k_', markersize=30, ecolor='gainsboro')
ax.set_ylim(0,100)

# anechoic vs reverberant
# prepare dataframe for plot
df['anechoic'] = df['anechoic'].astype('category')
df['anechoic'] = df['anechoic'].cat.rename_categories(['reverberant', 'anechoic'])

# get participant - wise environment data
anechoic = []
for participant in df.index.get_level_values('nametags').drop_duplicates().values:
    anechoic.append(df.xs(participant, level='nametags')['anechoic'].values[0])
anechoicMeans =df.groupby('nametags', dropna=False)['iaccs'].mean()

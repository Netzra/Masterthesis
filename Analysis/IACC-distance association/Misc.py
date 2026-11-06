import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("path")
meanResponses = df.groupby('actDist')['response'].mean().values
D = (3.65, 7.12, 10.68, 14.24, 17.8)
fig, ax = plt.subplots()
ax.plot(D, meanResponses, 'bo:', label='Mean')
ax.set_ylim(0,18.5)
ax.set_xlim(0,18.5)
ax.set_ylabel("response [vm]")
ax.set_xlabel('simulated distance [vm]')
perfect = range(0,19)
ax.plot(perfect,perfect,linestyle='--', c ='gainsboro', label='Perfect Performance')

df.set_index('subject', inplace=True)
participants = df.index.get_level_values('subject').drop_duplicates().values
for participant in participants:
    ax.plot(D, df.loc[participant].groupby('actDist')['response'].mean().values, color='gainsboro', linestyle = ':')
ax.legend()
plt.savefig('path')

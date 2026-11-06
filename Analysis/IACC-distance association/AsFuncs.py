import pandas as pd



def createPairwisePanda (df: pd.DataFrame)-> pd.DataFrame:
 df = df.reset_index(['subject', 'day', 'session', 'timestamp'])
 pairwise = {
  'subject': df['subject'].values[:-1],
  'day': df['day'].values[:-1],
  'session': df['session'].values[:-1],
  'number': [],
  'iacc': [],
  'iaccChange': [],
  'actDist': [],
  'distanceChange': [],
  'response': [],
  'responseChange': [],
  'correctChangeDetected': [],
  'soundfile': [],
  'reactionTime': []
 }

 experimentFilternumbers = df['stim_distance_ID'].values
 responses = df['resp_distance_VR'].values
 soundfiles = df['stim_filename'].values
 reactionTimes = df['reaction_time'].values
 IACCVALS = 100, 67.99, 42.54, 22.71, 3.45  #  IACCVALS = 1, .6799, .4254, .2271, .0345
 D = 3.65, 7.12, 10.68, 14.24, 17.8

 for index in range(df.__len__()-1):
  nextfilternumber = experimentFilternumbers[index+1]
  filternumber = experimentFilternumbers[index]
  nextTargetDistance = D[nextfilternumber]
  response = responses[index+1]
  iaccChange = round(IACCVALS[nextfilternumber] - IACCVALS[filternumber], 4)
  responseChange = response - responses[index]

  # takes the next filter and substracts current filter to calculate the change in IACCs, distance and responses
  pairwise['iacc'].append(IACCVALS[nextfilternumber])
  pairwise['iaccChange'].append(iaccChange)
  pairwise['actDist'].append(nextTargetDistance)
  pairwise['distanceChange'].append(nextTargetDistance - D[filternumber])
  pairwise['response'].append(response)
  pairwise['responseChange'].append(responseChange)
  pairwise['soundfile'].append(soundfiles[index+1])
  pairwise['reactionTime'].append(reactionTimes[index+1])

  if iaccChange == 0:
   if responseChange == 0:
    pairwise['correctChangeDetected'].append(1)
   elif responseChange > 0:
    pairwise['correctChangeDetected'].append(2)
   else:
    pairwise['correctChangeDetected'].append(-2)
  elif iaccChange > 0:
    if responseChange > 0:
     pairwise['correctChangeDetected'].append(1)
    elif responseChange == 0:
     pairwise['correctChangeDetected'].append(0)
    else:
     pairwise['correctChangeDetected'].append(-1)
  else:
   if responseChange < 0:
    pairwise['correctChangeDetected'].append(1)
   elif responseChange == 0:
    pairwise['correctChangeDetected'].append(0)
   else:
    pairwise['correctChangeDetected'].append(-1)

 pairwise['number'] = list(range(pairwise['iaccChange'].__len__()))

 pairwiseDf = pd.DataFrame(pairwise)
 pairwiseDf = pairwiseDf.set_index(['subject', 'day', 'session', 'number'])
 return pairwiseDf


def makeIACCchangeAbs (df: pd.DataFrame):
 absIACC = df[df['iaccChange'] < 0] * -1
 df.loc[df['iaccChange'] < 0, 'iaccChange'] =  absIACC
 return df

def iaccChange_Categories (df: pd.DataFrame):
 return df['iaccChange'].drop_duplicates().sort_values().values

def createDirectionDict (df: pd.DataFrame, iaccGroups:list = []):

 if not iaccGroups.__len__() == 0:
  iaccGroups = iaccChange_Categories(df)
 dfAbs = makeIACCchangeAbs(df.copy()).reset_index()
 # individual direction groups saved as series. Not all iaccGroups have each value.
 # Hopefully dataframe still gets instantiated correctly
 dirdict = {
  'subject': dfAbs['subject'].values[:iaccGroups.__len__()],
  'day': dfAbs['day'].values[:iaccGroups.__len__()],
  'session': dfAbs['session'].values[:iaccGroups.__len__()],
  'number': list(range(iaccGroups.__len__())),
  'iaccGroups': iaccGroups,
  'totalcounts': df.groupby('iaccChange').size().values,
  'illuClose': pd.Series(df[df['correctChangeDetected'] == -2].groupby('iaccChange').size(), index=iaccGroups, dtype='Int64'),
  'inverse': pd.Series(df[df['correctChangeDetected'] == -1].groupby('iaccChange').size(), index=iaccGroups, dtype='Int64'),
  'noDetec': pd.Series(df[df['correctChangeDetected'] == 0].groupby('iaccChange').size(), index=iaccGroups, dtype='Int64'),
  'correct': pd.Series(df[df['correctChangeDetected'] == 1].groupby('iaccChange').size(), index=iaccGroups, dtype='Int64'),
  'illuFar': pd.Series(df[df['correctChangeDetected'] == 2].groupby('iaccChange').size(), index=iaccGroups, dtype='Int64'),
 }
 directionDF = pd.DataFrame(dirdict)
 directionDF = directionDF.copy().set_index(['subject', 'day', 'session', 'number', 'iaccGroups'])
 directionDF = directionDF.fillna(0)
 return directionDF

def getDirectiongroupSeries (df:pd.DataFrame, tag):
 return df.loc[:, tag]

def getPercentages(s: pd.Series):
 return s.apply(lambda x: x/s.sum()*100)


def getIllusionDistribution (df: pd.DataFrame):
 sum = df.xs(0.0, level='iaccGroups')['illuClose'] + df.xs(0.0, level='iaccGroups')['illuFar']
 percentages = df.copy().apply(lambda x: x / sum * 100)
 print(percentages.index)
 return percentages.xs(0.0, level='iaccGroups')['illuClose'], percentages.xs(0.0, level='iaccGroups')['illuFar']

# Summed and percentages df across all participants, needs alldirections.csv loaded as Dataframe
def creatcsvsumNpercentageFromaDirecCSV(df: pd.DataFrame, session:int, direcCategory:str, path:str = 'path'):
 allCorrectDirection = df.xs(session, level='session')[['totalcounts', direcCategory]]
 summed = allCorrectDirection.groupby('iaccGroups').sum()
 percentages = summed.groupby('iaccGroups')[direcCategory].apply(lambda x: (x/summed['totalcounts'])*100).dropna()
 percentages.to_csv(f'{path}aPart{direcCategory}{session}%.csv')
 summed.to_csv(f'{path}aPart{direcCategory}{session}.csv')
 return 0


"""
from Auswertung.IACC_distanceAssociation.Current.AssociationIO import openCSVtoPandas
path = 'Path'
df = openCSVtoPandas(path)
test = createPairwisePanda(df.copy())
test3 = makeIACCchangeAbs(test.copy())
iaccGroups = iaccChange_Categories(test3)
test4 = createDirectionDict(test3, iaccGroups)
print(getIllusionDistribution(test4))
"""

"""
Developmentstuff

 print(
  pairwise['iaccChange'].__len__(),
  pairwise['subject'].__len__(),
  pairwise['day'].__len__(),
  pairwise['session'].__len__(),
  pairwise['number'].__len__(),
 )
"""



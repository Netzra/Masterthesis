from Auswertung.IACC_distanceAssociation.Current import AssociationFunctions as func, AssociationIO as io
import glob
import numpy as np
import pandas as pd



"""
Gerade df length funktioniert ordentlich
Ungerade nicht = letztes i letzte index stelle, aber funktioniert wenn man bei 1 beginnt

with dataframe.index.levels one can get access to all different values for indexes

Goal find out wether participants confused directions more in relation to the change of IACCs
look at standarddeviation grouped by iacc change, compare change of distance to change of response

When first running:

from Auswertung.IACC_distanceAssociation.Current import AssociationFunctions as func, AssociationIO as io
import glob
import numpy as np
import pandas as pd

parentdir = 'parentdirPATH'

pairwises = []
directiondfs = []
iaccChange_categories = np.array([0., 0.1926, 0.1983, 0.2545, 0.3201, 0.3909, 0.4528, 0.5746, 0.6454, 0.7729, 0.9655])


for file in glob.glob(parentdir+'/*.csv'):
    raw = io.openCSVtoPandas(file)
    pairwise = func.createPairwisePanda(raw.copy())
    abs = func.makeIACCchangeAbs(pairwise.copy())
    directions = func.createDirectionDict(abs, iaccChange_categories)

    pairwises.append(pairwise)
    directiondfs.append(directions)

allPairwise = pd.concat(pairwises)
allPairwise.sort_index().to_csv(path)
alldirections = pd.concat(directiondfs)
alldirections.sort_index().to_csv(path)



path = 'path'
iaccChange_categories = np.array([0., 0.1926, 0.1983, 0.2545, 0.3201, 0.3909, 0.4528, 0.5746, 0.6454, 0.7729, 0.9655])
df = io.readdirectionCSV(path)

# just taking final/ first session
dfjust1 = allPairwise.xs(1, level='session')
dfjust3 = allPairwise.xs(3, level='session')
"""

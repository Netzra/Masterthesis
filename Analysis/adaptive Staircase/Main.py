import adaptiveStaircaseAutoFunc as func
import adaptiveStaircaseIO as io
import glob
import numpy as np
import pandas as pd

"""
Notes:  adding a new participant to an existing Dataframe might be a bit expensive, when done as a row.
        Currently that is the case. However, flipDf allows to add a participant as a coloumn (easier than row).
        That might be more efficient for a few participants, but when many have to be added one might want to repeat
        the creation process for all of them. (Might take more computational time, but is less... exhausting)
"""

# instantiate all necessary collections as well as the parent dir for data
parentdir = 'path'
nametags = []
dataframes = []

for file in glob.glob(parentdir+'/*.txt'):
    participantdict = {
        "uso_cluster": [],
        "n_reversals": [],
        "means": [],
        "thresholds": [],
        "iaccs": []
    }

    currentFile = io.openSlabResultsFile(file)
    nametag = func.getName(currentFile)
    nametags.append(func.getName(currentFile))

    print(file)

    # calculate all the necessary data for a single participant
    participantdict["uso_cluster"] = func.findTag(currentFile, 'USO_cluster', True)
    reversalItens = func.findTag(currentFile, 'reversal_intensities', True)
    participantdict["means"] = [round(np.mean(x), 2) for x in reversalItens]
    participantdict["n_reversals"] = [len(x) for x in reversalItens]
    participantdict["thresholds"] = func.calcThresholdsAdaptiveStaircaseVRMasterarbeit(reversalItens)
    participantdict["iaccs"] = func.calculateIACCadaptiveStaircase(participantdict["thresholds"])

    print(participantdict["uso_cluster"],
          participantdict['n_reversals'],
          participantdict["iaccs"],
          participantdict["means"],
          nametag)

    # collect the data from one participant
    dataframes.append(pd.DataFrame(participantdict))

# List all participants nametags used in current data evaluation
print(nametags)

# generate pandas Dataframe with all participants
allParticipants = io.combineDFsintoSinglePanda(dataframes, nametags)

print(allParticipants.sort_index())

# save combined Dataframe for all participants
io.writePandaToCSV(allParticipants.sort_index(), "path")




"""
command
dataframe.xs(value, level = "Name of level") to select Subdatasets based on a single index.
"""


import slab
import numpy as np
import pandas as pd

"""
The file takes a singular txt file and calculates the thresholds for each individual staircase
IACC calculation:   the adaptive staircase threshold returns a non- rounded float number. 
                    The calculation of IACC values is done by first rounding the threshhold to the nearest .5/.0 float ~
                    value and second either immediately picking the IACC value from a constant tuple (.0) or calculating ~ 
                    it by (IACC_upperFilter - IACC_lowerFilter)/2 + IACC_lowerFilter
Return:             Not yet determined (pandas Datafile most likely. probably separated from other functions)
"""


def findTag(lst: list, tag: str, removeTag: bool = True) -> list:
    searchResults = []
    for line in lst:
        if line.keys().__contains__(tag):
            if removeTag:
                searchResults.append(line[tag])
            else:
                searchResults.append(line)
    return searchResults


def calcThresholdsAdaptiveStaircaseVRMasterarbeit(lst: list) -> object:
    manipulatedThresholds = []
    for line in lst:
        rawThreshhold = np.mean(line)
        fraction = rawThreshhold % 1

        if rawThreshhold % .5 == 0:
            manipulatedThresholds.append(rawThreshhold)
        elif fraction < 0.25 or fraction >= 0.75:
            manipulatedThresholds.append(round(rawThreshhold))
        else:
            manipulatedThresholds.append((rawThreshhold // 1) + .5)
    return manipulatedThresholds


def printTags(lst: list) -> object:
    tags = []
    for line in lst:
        for tag in list(line.keys()):
            if not tags.__contains__(tag):
                tags.append(tag)
    return tags


def calculateIACCadaptiveStaircase(lst: list):
    IACCVALUESADAPTIVESTAIRCASE = np.array(
        [1, .9951, .9805, .9567, .9242, .8841, .8373, .7848, .7279, .6676, .6051, .5412, .4768, .4126, .3493, .2873,
         .2271, .1689, .1128, .0592, .0345])
    iaccs = []
    for threshold in lst:
        if threshold % 1 == 0:
            iaccs.append(round(IACCVALUESADAPTIVESTAIRCASE[int(threshold)] * 100, 2))
        else:
            upperThresh = IACCVALUESADAPTIVESTAIRCASE[int(threshold - .5)]
            lowerThresh = IACCVALUESADAPTIVESTAIRCASE[int(threshold + .5)]
            iaccs.append(round(((upperThresh - lowerThresh) / 2 + lowerThresh) * 100, 2))

    return iaccs

def getName(lst:list):
    return findTag(lst, printTags(lst)[0], True)[0]

def flipDf(df:pd.DataFrame):
    return df.T


'''
import adaptiveStaircaseIO

path = PATH
testFile = adaptiveStaircaseIO.openSlabResultsFile(path)
print(printTags(testFile))
reversalIntens = findTag(testFile, 'reversal_intensities', True)
print(reversalIntens)
print([np.mean(intens) for intens in reversalIntens])
thresholds = calcThresholdsAdaptiveStaircaseVRMasterarbeit(reversalIntens)
print(thresholds)
print(calculateIACCadaptiveStaircase(thresholds))

#combining Dataframes
df1 = pd.DataFrame([["c", 3], ["d", 4]], columns=["letter", "number"])
df2 = pd.DataFrame([["c", 4], ["d", 6]], columns=["letter", "number"])

print(pd.concat([df1, df2], keys=[2,1]))
'''

import slab
import pandas as pd

def openSlabResultsFile(path: str) -> list:
    return slab.ResultsFile.read_file(path)

def openCSVtoPanda(path):
    return pd.read_csv(path, index_col=["nametags", "number"]).sort_index()


def combineDFsintoSinglePanda (lst: list, nametags):
    return pd.concat(lst, keys=nametags, names=["nametags", "number"])


def writePandaToCSV (df: pd.DataFrame, path: str) -> None:
    df.to_csv(path)
    return 0


"""
path = PATH
test = openCSVtoPanda(path)
print(test)
"""

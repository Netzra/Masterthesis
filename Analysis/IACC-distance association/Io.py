import pandas as pd

def openCSVtoPandas(path:str)->pd.DataFrame:

    # load dataframe
    dataframe = pd.read_csv(path)

    # get rid of unnecessary columns
    del dataframe['phase'], dataframe['run'], dataframe['room'], dataframe['is_manipulated_distance_law']

    # transform timestamps to datetime datatype
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    # reindex timestamp stays column to support timedifference (calculation)
    dataframe = dataframe.set_index(['subject', 'day', 'session', 'timestamp'])

    return dataframe


def readdirectionCSV (path: str):
    return pd.read_csv(path).set_index(['subject', 'day', 'session', 'number', 'iaccGroups'])


"""
path = 'path'
test = openCSVtoPandas(path)
print(test, test.index)
"""

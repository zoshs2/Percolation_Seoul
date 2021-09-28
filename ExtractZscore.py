import pandas as pd
import numpy as np

def extract_Zscore_df(dataset):
    def Zscore(x):
        return (x[0]-x[1]) / x[2]

    MEAN_DF = dataset.groupby(['LINK_ID'])['PRCS_SPD'].mean().reset_index()
    STD_DF = dataset.groupby(['LINK_ID'])['PRCS_SPD'].std().reset_index()
    dataset = dataset.merge(MEAN_DF, on='LINK_ID').rename(columns={'PRCS_SPD_x':'PRCS_SPD', 'PRCS_SPD_y':'MEAN'})
    dataset = dataset.merge(STD_DF, on='LINK_ID').rename(columns={'PRCS_SPD_x':'PRCS_SPD', 'PRCS_SPD_y':'STD'})
    dataset['ratio'] = dataset[['PRCS_SPD', 'MEAN', 'STD']].apply(Zscore, axis=1)
    dataset = dataset.drop(['MEAN', 'STD'], axis=1)

    return dataset
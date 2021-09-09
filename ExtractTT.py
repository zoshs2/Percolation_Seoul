import pandas as pd
import numpy as np

def extract_travelT_df(dataset, distDF): 
    '''
    Based on the Great Circle Distance of each links and mean velocity dataset,
    this module extracts the expected travel time of each links at certain time.
    '''
    def CalTravelTime(x):
        H2M_UNIT_FACTOR = round(1/60, 6)
        tt = round(x[1] / (x[0] * H2M_UNIT_FACTOR), 5)
        return tt
    
    if not dataset[dataset['PRCS_SPD']==0].empty:
        zero_speed = dataset[dataset['PRCS_SPD']==0].shape[0]
        print("'{}' links with the speed of 0-km/h are found. We rule out that links.".format(zero_speed))

    dataset = dataset[dataset['PRCS_SPD']!=0].reset_index(drop=True)
    dataset = dataset.merge(distDF, on='LINK_ID')
    dataset['ratio'] = dataset[['PRCS_SPD', 'DIST']].apply(CalTravelTime, axis=1)
    dataset = dataset.drop('PRCS_SPD', axis=1) # 1
    dataset = dataset.rename(columns={'ratio':'PRCS_SPD'}) # 2
    return dataset
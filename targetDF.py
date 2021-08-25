import pandas as pd

def targetDF(dataset, YEAR, MONTH, DAY, HOUR=False, MINUTE=False) -> pd.DataFrame:
    '''
    Return pd.DataFrame with only data that we concerned.

    Example
    -------
    In[0] date_dataset = targetDF(dataset, 2021, 2, 1)
    In[1] date_dataset = extract_ratio_df(date_dataset) # Generate a ratio column
    In[2] time_dataset = targetDF(date_dataset, 2021, 2, 1, 9, 0) # 2021-02-01 / 09:00 AM 
    In[3] CheckOverRatio(time_dataset) # Check over ratio raws & do the correction by inplacing.
    '''

    if (HOUR is not False) & (MINUTE is not False):
        vel_target = dataset[(dataset['PRCS_YEAR']==YEAR) & (dataset['PRCS_MON']==MONTH) & (dataset['PRCS_DAY']==DAY) & (dataset['PRCS_HH']==HOUR) & (dataset['PRCS_MIN']==MINUTE)]
        vel_target = vel_target.reset_index(drop=True)
        return vel_target

    vel_target = dataset[(dataset['PRCS_YEAR']==YEAR) & (dataset['PRCS_MON']==MONTH) & (dataset['PRCS_DAY']==DAY)]
    vel_target = vel_target.reset_index(drop=True)
    return vel_target
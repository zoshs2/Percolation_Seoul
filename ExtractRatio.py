def ExtractRatio(full_df:pd.DataFrame) -> pd.DataFrame():
    '''
    input DataFrame must have at least full-time (a resolution of 5 min) values for one day.
    This Function extracts the ratio in terms of its 95% percentile value for that day.

    Note
    ---------
    For too long period day, dataset could be trouble in memory and take a long time, which is inefficienct.
    So we recommend that you should use this function by cutting the dataset for a proper period of days.
    See Example.

    Example
    --------
    day_dataset = dataset[(dataset["PRCS_YEAR"]==2021) & (dataset["PRCS_MON"]==2) & (dataset["PRCS_DAY"]==1)]
    day_datset = ExtractRatio(day_dataset)
    
    # With a module of SpatialRatioDist, you can follow this steps below.
    target_data = day_dataset[(day_dataset["PRCS_HH"]==9) & (day_dataset["PRCS_MIN"]==0)] # If we concern about 9:00 AM.
    SpatialRatioDist(slink_loc, target_data, truncate=True, minval=0.2, maxval=1)
    '''
    
    LMV = full_df.loc[:, ['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'LINK_ID', 'PRCS_SPD']].groupby(['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'LINK_ID']).quantile(0.95).rename({'PRCS_SPD':'LMV'}, axis='columns')
    LMV = LMV.reset_index().sort_values(['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'LINK_ID'], ascending=True)
    full_df = full_df.sort_values(['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'LINK_ID'], ascending=True)
    
    one_day = int(full_df.shape[0] / LMV.shape[0])
    if one_day != 288: # 5 min resolution; One day = 24hours * 60 mins / 5 min resolution = 288 
        raise Warning("DataFrame seems to have some missing time-series data")

    start = 0
    ratio_list = []
    for lmv in LMV['LMV'].values:
        rslt = full_df[start:start+one_day]['PRCS_SPD'] / lmv
        rslt = rslt.to_list()
        ratio_list.extend(rslt)
        start += one_day
        
    full_df['ratio'] = ratio_list
    return full_df
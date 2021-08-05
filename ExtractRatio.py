def ExtractRatio(full_df:pd.DataFrame) -> pd.DataFrame():
    '''
    input DataFrame must have at least full-time (a resolution of 5 min) values for one day.
    This Function extracts the ratio in terms of its 95% percentile value for that day.
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
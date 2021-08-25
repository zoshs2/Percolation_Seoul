import pandas as pd

def IdentifyBN(Qc_dataset, ratioDF) -> pd.DataFrame:
    # Identify bottleneck (BN)
    Y, M, D, h, m = ratioDF.loc[0, ['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    qc = Qc_dataset[(Qc_dataset['year']==Y) & (Qc_dataset['month']==M) & (Qc_dataset['date']==D) & (Qc_dataset['hour']==h) & (Qc_dataset['min']==m)]['q_c'].values[0]
    sortDF = ratioDF.sort_values('ratio').dropna().reset_index(drop=True)
    try:
        BeforeQcIdx = sortDF[sortDF['ratio']==qc].index.values[0] -  1
        BeforeQcRatio = sortDF.iloc[BeforeQcIdx, :]['ratio']
        bottleneck = ratioDF[ratioDF['ratio']==BeforeQcRatio]
    
    except IndexError:
        return False
    
    return bottleneck
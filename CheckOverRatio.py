import pandas as pd

def CheckOverRatio(RatioDF:pd.DataFrame, verbose=True):
    # Raw(s) with ratio over 1 sets to 1 by inplacing.
    over_idx = RatioDF[RatioDF['ratio']>1].index
    if over_idx.empty and verbose is True:
        return print("No Update")

    else:
        RatioDF.loc[over_idx, 'ratio'] = 1.0
        if verbose is True:
            return print("{} of {} have been updated by value of '1.0'".format(len(over_idx), len(RatioDF)))
        return
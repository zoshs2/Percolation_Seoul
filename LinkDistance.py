import pandas as pd
import numpy as np
from geopy.distance import distance

def LinkDistance(loc_df):
    '''
    Using the GIS coordinates of each links contained on loc_df,
    this module extract the Great Circle Distance between start & end nodes in units of kilometre.
    '''
    def CalDistance(x):
        p1 = (x[0], x[1])
        p2 = (x[2], x[3])
        dist = distance(p1, p2).kilometers
        return dist
    
    st_pos = loc_df.groupby('link_id').nth(0).reset_index().loc[:, ['link_id', 'lat', 'lon']]
    ed_pos = loc_df.groupby('link_id').nth(-1).reset_index().loc[:, ['link_id', 'lat', 'lon']]
    loc_df = st_pos.merge(ed_pos, on='link_id')
    loc_df['DIST'] = loc_df[['lat_x', 'lon_x', 'lat_y', 'lon_y']].apply(CalDistance, axis=1)
    if not loc_df[loc_df['DIST']==0].empty:
        zero_dist = list(loc_df[loc_df['DIST']==0]['link_id'].values)
        print("We found '{}' Link(s) with 'zero(0)' distance.".format(len(zero_dist)))
        print("Zero Distance Link: ", zero_dist)
        loc_df = loc_df[loc_df['DIST']!=0].reset_index(drop=True)

    loc_df = loc_df.drop(['lat_x', 'lon_x', 'lat_y', 'lon_y'], axis=1)
    loc_df = loc_df.rename(columns={'link_id':'LINK_ID'})
    return loc_df
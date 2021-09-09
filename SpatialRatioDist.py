from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
 
 def SpatialRatioDist(loc_df:pd.DataFrame, ratio_df:pd.DataFrame, c_map=plt.cm.jet_r, truncate=False, minval=0.2, maxval=0.8, savefig:'file_name'=False) -> plt.show():
        ''' Display the Spatial Distribution of Link Qualities on the geometric locations of Seoul Roads.
    Parameters
    ---------
    loc_df : pd.DataFrame
        DataFrame which contains "Geometric Location" for each Seoul Links. (Longitute & Latitude)
    
    ratio_df : pd.DataFrame
        DataFrame which contains "Link Quality" for each Seoul Links.

    c_map : plt.cm.<colormap>
        Colormap which will be applied to the range of link qualities.

    truncate : default is "False"
        An Option to use the truncated colormap.

    minval : default is 0.2 (A range of 0.0 ~ 1.0)
        Minimum value that would truncate the colormap.

    maxval : default is 0.8 (A range of 0.0 ~ 1.0)
        Maximum value that would truncate the colormap.
    
    Notes
    ------
    ** Some Pre-processing before plotting **
    
    In order to plot the Spatial Ratio Distribution of the links based on their REAL location(lon, lat), we 
    should compare their included informations with each other (i.e., loc_df and ratio_df). 
    Up to 'Second Stage', it is the process that organizes matching link(s), not non-matching link(s).
    '''
    # We can only use a certain part of the colormap by this function.
    def truncate_colormap(cmap, minval=minval, maxval=maxval, n=100):
        '''
        Parameters
        -------------
        cmap : plt.cm.<colormap>
            Colormap used in 'SpatialRatioDist' function.

        minval : Minimum value that would truncate the colormap. (A range of 0.0 ~ 1.0)

        maxval : Maximum value that would truncate the colormap. (A range of 0.0 ~ 1.0)
        '''
        new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
            cmap(np.linspace(minval, maxval, n)))
        return new_cmap

    # First Stage: Find non-matching link(s)
    slink_id = loc_df['link_id'].unique()
    noexist_id = []
    for vel_id in ratio_df['LINK_ID'].values:
        if vel_id in slink_id:
            continue

        else:
            noexist_id.append(vel_id)
    else:
        print("Matching Check Done. We found non-matched '{}' link(s) between Location info. & Ratio info. ".format(len(noexist_id)))
        if len(noexist_id) != 0:
            print("Non-matching Link: ", noexist_id)

    # Second Stage: Organize matching link(s) only. 
    dropIdx = ratio_df[ratio_df['LINK_ID'].isin(noexist_id)].index
    ratio_df = ratio_df.drop(dropIdx).reset_index(drop=True)
    # In addition, we decompose the dataset into that of link(s) not-having NaN Ratio.
    nanIdx = ratio_df[ratio_df['ratio'].isna()].index
    if not nanIdx.empty:
        nanLink = ratio_df.loc[nanIdx, 'LINK_ID'].values
        print("NaN Ratio Link: ", nanLink)
        ratio_df = ratio_df.drop(nanIdx).reset_index(drop=True)
    
    else:
        print("Nothing link(s) with NaN ratio")

    # Third Stage: Plot the ratio spatial distribution with colormap
    ratio_df = ratio_df.sort_values('ratio').reset_index(drop=True)

    TIME = ratio_df.loc[0, ['PRCS_YEAR','PRCS_MON','PRCS_DAY','PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    TIME = datetime(TIME[0], TIME[1], TIME[2], TIME[3], TIME[4])
    filetime_name = str(TIME.strftime("%Y%m%d_%H%M%p"))
    YEAR_MON_DAY = TIME.strftime("%Y-%m-%d")
    HOUR_MIN = TIME.strftime("%H:%M %p")

    c_range = ratio_df['ratio'].values # The range of Link Qualities.
    norm = mpl.colors.Normalize(vmin=np.min(c_range), vmax=np.max(c_range))

    # Truncate Check
    if truncate == True:
        c_map = truncate_colormap(c_map, minval=minval, maxval=maxval, n=len(c_range))
        colors = c_map(norm(c_range))
    
    else:
        colors = c_map(norm(c_range))

    fig = plt.figure(facecolor='w', figsize=(18,15))
    for i, sid in enumerate(ratio_df['LINK_ID'].values):
        target_row = ratio_df[ratio_df['LINK_ID']==sid]
        
        x = loc_df[loc_df['link_id']==sid]['lon']
        y = loc_df[loc_df['link_id']==sid]['lat']
        plt.plot(x, y, linewidth=3.2, color=colors[i])
    
    c_bar = fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=c_map), aspect=50)
    c_bar.ax.set_ylabel('Link quality (Ratio)', fontsize = 20)
    plt.setp(c_bar.ax.yaxis.get_ticklabels(), fontsize=16)
    
    plt.text(126.8, 37.675, YEAR_MON_DAY, size=28, fontweight='semibold', fontstyle='italic')
    plt.text(126.8, 37.665, HOUR_MIN, size=28, fontweight='semibold', fontstyle='italic')
    
    plt.xlabel('Longitude', fontsize=20)
    plt.ylabel('Latitude', fontsize=20)
    if savefig is not False:
        filename = savefig + "_SpatialRatioDist_" + filetime_name + ".png"
        print(filename, " saved on ", os.getcwd())
        plt.savefig(filename)
    plt.show()
 from datetime import datetime
 
 def SpatialRatioDist(loc_df:pd.DataFrame, ratio_df:pd.DataFrame, c_map=plt.cm.jet_r) -> plt.show():
    ''' Display the Spatial Distribution of Link Qualities on the geometric locations of Seoul Roads.
    Parameters
    ---------
    loc_df : pd.DataFrame
        DataFrame which contains "Geometric Location" for each Seoul Links. (Longitute & Latitude)
    ratio_df : pd.DataFrame
        DataFrame which contains "Link Quality" for each Seoul Links.

    c_map : plt.cm.<colormap>
        Colormap which will be applied to the range of link qualities.
    
    Notes
    ------
    ** Some Pre-processing before plotting **
    
    In order to plot the Spatial Ratio Distribution of the links based on their REAL location(lon, lat), we 
    should compare their included informations with each other (i.e., loc_df and ratio_df). 
    Up to 'Second Stage', it is the process that organizes matching link(s), not non-matching link(s).
    '''
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
    dropIdx = ratio_df[ratio_df['LINK_ID'].isin(nonexist_id)].index
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
    YEAR_MON_DAY = TIME.strftime("%Y-%m-%d")
    HOUR_MIN = TIME.strftime("%H:%M %p")

    c_range = ratio_df['ratio'].values # The range of Link Qualities.
    colors = c_map(c_range) 
    norm = mpl.colors.Normalize(vmin=np.min(c_range), vmax=np.max(c_range))

    fig = plt.figure(facecolor='w', figsize=(18,15))
    for i, sid in enumerate(ratio_df['LINK_ID'].values):
        target_row = ratio_df[ratio_df['LINK_ID']==sid]
        
        x = loc_df[loc_df['link_id']==sid]['lon']
        y = loc_df[loc_df['link_id']==sid]['lat']
        plt.plot(x, y, linewidth=3, color=colors[i])
    
    c_bar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=c_map), aspect=50)
    c_bar.ax.set_ylabel('Link quality (Ratio)', fontsize = 20)
    plt.setp(c_bar.ax.yaxis.get_ticklabels(), fontsize=16)
    
    plt.text(126.8, 37.675, YEAR_MON_DAY, size=28, fontweight='semibold', fontstyle='italic')
    plt.text(126.8, 37.665, HOUR_MIN, size=28, fontweight='semibold', fontstyle='italic')
    
    plt.xlabel('Longitude', fontsize=20)
    plt.ylabel('Latitude', fontsize=20)
    plt.show()
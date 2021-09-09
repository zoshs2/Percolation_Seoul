import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.nonparametric.kernel_regression import KernelReg

def RandLinkVelDist(date_dataset, sample=20, reg=False, time_step=5, savefig:'file_name'=False):
    '''
    Display the circadian velocity distribution of randomly-selected road samples.
    '''
    VEL_RESOLUTION = 5
    timestep = int(time_step / VEL_RESOLUTION)
    
    TIME = date_dataset.loc[0, ['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    TIME = datetime(TIME[0], TIME[1], TIME[2], TIME[3], TIME[4])
    filename_date = "s" + str(sample) + "_" + str(TIME.strftime("%Y%m%d"))
    
    RandData = date_dataset[date_dataset['LINK_ID'].isin(np.random.choice(date_dataset['LINK_ID'].unique(), sample))].reset_index(drop=True)
    TimeIdx = RandData.groupby(['PRCS_HH', 'PRCS_MIN'])['PRCS_SPD'].mean().index # mean() is just used to get a groupy time('Hour', 'Min') index.
    time_xaxis = list(map(lambda x : str(format(x[0], '02d'))+':'+str(format(x[1], '02d')), TimeIdx))
    time_xaxis = [datetime.strptime(i, '%H:%M') for  i in time_xaxis]
    RandIDs = RandData['LINK_ID'].unique()

    fig = plt.figure(facecolor='w', figsize=(15, 8))
    ax = plt.gca() # Get the Current Axes (GCA)
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, sample)]
    for i, ID in enumerate(RandIDs):
        RandOne = RandData[RandData['LINK_ID']==ID].sort_values(by=['PRCS_HH', 'PRCS_MIN'])
        VelHist = RandOne['PRCS_SPD'].values
        
        if reg is True:
            VelShape = VelHist.shape[0]
            kde = KernelReg(endog=VelHist, exog=np.arange(VelShape), var_type='c', bw=[5])
            estimator = kde.fit(np.arange(VelShape))
            estimator = np.reshape(estimator[0], VelShape)
            plt.plot(time_xaxis, estimator, c=colors[i], label=str(ID))
            continue
        
        plt.plot(time_xaxis[::timestep], VelHist[::timestep], c=colors[i], label=str(ID))
        
    fmt = mpl.dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()
    
    ax.set_ylabel('Velocity (km/h)', fontsize=18)
    ax.set_xlabel('Time', fontsize=18)
    if savefig is not False:
        filename = savefig + "_RandLinkVelDist_" + filename_date
        if reg is True:
            filename = "(Reg)" + filename
        
        with open(filename+'.txt', 'w') as f:
            for ID in RandIDs:
                f.write("{}\n".format(ID))
                
        print(filename, ".txt saved on ", os.getcwd())
        print(filename, ".png saved on ", os.getcwd())
        plt.savefig(filename + ".png")

    plt.show()
    return
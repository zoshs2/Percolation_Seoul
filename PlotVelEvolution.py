import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

def PlotVelEvolution(Vel_dataset, time_step=5, ddof=0, shaded_error=False, savefig:'file_name'=False):
    # Vel_dataset must contain a 'day' column.
    
    Vel_dataset = Vel_dataset.groupby(['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'PRCS_HH', 'PRCS_MIN', 'day'])['PRCS_SPD'].mean().reset_index()
    VEL_RESOLUTION = 5
    timestep = int(time_step / VEL_RESOLUTION)

    vel_weekend = Vel_dataset[(Vel_dataset['day']=='Sat') | (Vel_dataset['day']=='Sun')]
    vel_weekday = Vel_dataset[(Vel_dataset['day']!='Sat') & (Vel_dataset['day']!='Sun')]

    std_weekend = vel_weekend.groupby(['PRCS_HH','PRCS_MIN']).agg(np.std, ddof=ddof) 
    std_weekend = std_weekend.reset_index()['PRCS_SPD']
    std_weekday = vel_weekday.groupby(['PRCS_HH','PRCS_MIN']).agg(np.std, ddof=ddof)
    std_weekday = std_weekday.reset_index()['PRCS_SPD']

    vel_weekend = vel_weekend.groupby(['PRCS_HH','PRCS_MIN'])['PRCS_SPD'].mean()
    time_xaxis = list(map(lambda x : str(format(x[0], '02d'))+':'+str(format(x[1], '02d')), vel_weekend.index))
    time_xaxis = [datetime.strptime(i, '%H:%M') for i in time_xaxis]

    weekend_yaxis = vel_weekend.reset_index()['PRCS_SPD']
    vel_weekday = vel_weekday.groupby(['PRCS_HH','PRCS_MIN'])['PRCS_SPD'].mean()
    weekday_yaxis = vel_weekday.reset_index()['PRCS_SPD']

    fig = plt.figure(facecolor='w', figsize=(8,8))
    ax = plt.gca()
    
    if shaded_error is True:
        plt.plot(time_xaxis[::timestep], weekday_yaxis[::timestep], c='green', marker='s', markerfacecolor='w', label='Weekdays')
        plt.fill_between(time_xaxis[::timestep], weekday_yaxis[::timestep]-std_weekday[::timestep], weekday_yaxis[::timestep]+std_weekday[::timestep], color='green', alpha=0.5)
        plt.plot(time_xaxis[::timestep], weekend_yaxis[::timestep], c='purple', marker='s', markerfacecolor='w', label='Weekends')
        plt.fill_between(time_xaxis[::timestep], weekend_yaxis[::timestep]-std_weekend[::timestep], weekend_yaxis[::timestep]+std_weekend[::timestep], color='purple', alpha=0.5)
    
    else:
        plt.errorbar(time_xaxis[::timestep], weekday_yaxis[::timestep], std_weekday[::timestep], capsize=4, markersize=7, c='green', marker="s", alpha=1.0, label='Weekdays')
        plt.errorbar(time_xaxis[::timestep], weekend_yaxis[::timestep], std_weekend[::timestep], capsize=4, markersize=7, c='purple', marker="s", alpha=1.0, label='Weekends')
    
    plt.legend(loc='lower left', prop={'size': 16})
    fmt = mpl.dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()

    ax.set_ylabel('Velocity (m/s)', fontsize=18)
    ax.set_xlabel(r'$Time$', fontsize=18)
    plt.grid()
    if savefig is not False:
        savefig = savefig + "(Shaded)" if shaded_error else savefig + "(BarError)"
        filename = savefig + "_PlotVelEvolution_TimeStep(" + str(time_step) + "min).png"
        plt.savefig(filename)
        print(filename, " saved on ", os.getcwd()) 

    plt.show()
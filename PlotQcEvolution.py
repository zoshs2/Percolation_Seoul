def PlotQcEvolution(Qc_dataset, time_step=10, ddof=0, shaded_error=False, savefig:'file_name'=False):
    QC_RESOLUTION = 10 # the unit of minute(m);; QC_RESOLUTION = 10 means that Qc_dataset contains q_c over the day with '10 minute' interval.
    time_step = int(time_step / QC_RESOLUTION)

    qc_weekend = Qc_dataset[(Qc_dataset['day']=='Sat') | (Qc_dataset['day']=='Sun')]
    qc_weekday = Qc_dataset[(Qc_dataset['day']!='Sat') & (Qc_dataset['day']!='Sun')]

    # the divisor N - ddof(degree of freedom); 
    # This has a divisor of N-1, and is used when you have a subset of data from a larger set.
    std_weekend = qc_weekend.groupby(['hour','min']).agg(np.std, ddof=ddof) 
    std_weekend = std_weekend.reset_index()['q_c']
    std_weekday = qc_weekday.groupby(['hour','min']).agg(np.std, ddof=ddof)
    std_weekday = std_weekday.reset_index()['q_c']

    qc_weekend = qc_weekend.groupby(['hour','min'])['q_c'].mean()
    time_xaxis = list(map(lambda x : str(format(x[0], '02d'))+':'+str(format(x[1], '02d')), qc_weekend.index))
    time_xaxis = [datetime.strptime(i, '%H:%M') for i in time_xaxis]

    weekend_yaxis = qc_weekend.reset_index()['q_c']
    qc_weekday = qc_weekday.groupby(['hour','min'])['q_c'].mean()
    weekday_yaxis = qc_weekday.reset_index()['q_c']

    fig = plt.figure(facecolor='w', figsize=(8,8))
    ax = plt.gca()

    if shaded_error is True:
        plt.plot(time_xaxis[::time_step], weekday_yaxis[::time_step], c='green', marker='s', markerfacecolor='w', label='Weekdays')
        plt.fill_between(time_xaxis[::time_step], weekday_yaxis[::time_step]-std_weekday[::time_step], weekday_yaxis[::time_step]+std_weekday[::time_step], color='green', alpha=0.5)
        plt.plot(time_xaxis[::time_step], weekend_yaxis[::time_step], c='purple', marker='s', markerfacecolor='w', label='Weekends')
        plt.fill_between(time_xaxis[::time_step], weekend_yaxis[::time_step]-std_weekend[::time_step], weekend_yaxis[::time_step]+std_weekend[::time_step], color='purple', alpha=0.5)
    
    else:
        plt.errorbar(time_xaxis[::time_step], weekday_yaxis[::time_step], std_weekday[::time_step], capsize=4, markersize=7, c='green', marker="s", alpha=1.0, label='Weekdays')
        plt.errorbar(time_xaxis[::time_step], weekend_yaxis[::time_step], std_weekend[::time_step], capsize=4, markersize=7, c='purple', marker="s", alpha=1.0, label='Weekends')
    
    plt.legend(loc='lower left', prop={'size': 16})
    fmt = mpl.dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate()

    ax.set_ylabel(r'$q_{c}$', fontsize=18)
    ax.set_xlabel(r'$Time$', fontsize=18)
    plt.grid()
    if savefig is not False:
        savefig = savefig + "(Shaded)" if shaded_error else savefig + "(BarError)"
        filename = savefig + "_PlotQcEvolution_TimeStep(" + str(time_step) + "min).png"
        plt.savefig(filename)
        print(filename, " saved on ", os.getcwd()) 
    plt.show()
def PlotAmeliorateBN(Qc_dataset, NodeLinkDF, time_dataset, BN_DF, interval=100, with_random=False, savefig:'file_name'=False) -> 'Ameliorated_QcList':
    fig = plt.figure(facecolor='w', figsize=(7,7))

    QcRList_set = {'Bottleneck':[], 'Random':[], 'BC':[]}
    alpha_range = 1 + np.linspace(0,0.22,51)
    Ameliorated_QcList = []

    Y, M, D, h, m = time_dataset.loc[0, ['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    TIME = datetime(Y, M, D, h, m)
    YMDHM = TIME.strftime("%Y-%m-%d / %H:%M %p")
    filetime_name = str(TIME.strftime("%Y%m%d_%H%M%p"))

    origin_qc = Qc_dataset[(Qc_dataset['year']==Y) & (Qc_dataset['month']==M) & (Qc_dataset['date']==D) & (Qc_dataset['hour']==h) & (Qc_dataset['min']==m)]['q_c'].values[0]
    # print(origin_qc)
    
    while with_random:
        randomDF = time_dataset.copy()
        random_link = randomDF[randomDF['ratio'] < origin_qc].sample(1)
        if random_link['LINK_ID'].values[0] != BN_DF['LINK_ID'].values[0]:
            break

    BN_Idx = time_dataset[time_dataset['LINK_ID']==BN_DF['LINK_ID'].values[0]].index[0]
    BN_OriginRatio = BN_DF['ratio'].values[0]
    flag = False

    for i, alpha in enumerate(alpha_range):
        if flag is True:
            Ameliorated_QcList.append(PreviousQc)
            continue
        
        improved_ratio = (BN_OriginRatio * alpha)
        time_dataset.iloc[BN_Idx,time_dataset.columns.get_loc('ratio')] = improved_ratio # DF.iloc[IDX, :]['COL'] = x 이런 식으로는 바뀔 때도 있고, 안 바뀔때도 잇음.. 이상함..
        Ameliorated_Qc = SinglePP(NodeLinkDF, time_dataset, q_step=interval)
        Ameliorated_QcList.append(Ameliorated_Qc)
        
        if i > 0:
            PreviousQc = Ameliorated_QcList[i-1]
        
            if Ameliorated_Qc == PreviousQc:
                print("Saturation!!")
                SaturatedIdx = i
                flag=True
                continue
    else:
        Ratio_Qc = np.array(Ameliorated_QcList) / origin_qc
        QcRList_set['Bottleneck'] = Ratio_Qc

    if with_random:
        print(">>> Random Process Starts")
        flag = False
        RandomLink_QcList= []
        for i, alpha in enumerate(alpha_range):
            if flag is True:
                RandomLink_QcList.append(PreviousQc)
                continue
            
            RandomRatio = random_link['ratio'].values[0]
            improved_ratio = (RandomRatio * alpha)
            randomDF.iloc[random_link.index, randomDF.columns.get_loc('ratio')] = improved_ratio # DF.iloc[IDX, :]['COL'] = x 이런 식으로는 바뀔 때도 있고, 안 바뀔때도 잇음.. 이상함..
            RandomLink_Qc = SinglePP(NodeLinkDF, randomDF, q_step=interval)
            RandomLink_QcList.append(RandomLink_Qc)
            
            if i > 2:
                PreviousQc = RandomLink_QcList[i-3]
            
                if RandomLink_Qc == PreviousQc:
                    print("Saturation!!")
                    flag=True
                    continue
        else:
            RandomResult = np.array(RandomLink_QcList) / origin_qc
            QcRList_set['Random'] = RandomResult
            plt.plot(alpha_range[:SaturatedIdx+5], QcRList_set['Random'][:SaturatedIdx+5], marker='^', markersize=10, color='purple', alpha=0.7, label='Random')
     
    plt.plot(alpha_range[:SaturatedIdx+5], QcRList_set['Bottleneck'][:SaturatedIdx+5], marker='s', markersize=10, color='green', alpha=0.7, label='Bottleneck')
    
    text_x = alpha_range[SaturatedIdx-4]
    text_y = (QcRList_set['Bottleneck'][2] + QcRList_set['Bottleneck'][1]) / 2
    plt.text(text_x, text_y , YMDHM, size=21, fontweight='semibold', fontstyle='italic')

    plt.ylabel(r"$q'_{c}/q_{c}$", fontsize=17)
    plt.xlabel(r"$1+\alpha$", fontsize=17)
    plt.legend(prop={'size':14})
    plt.grid()

    if savefig is not False:
        filename = savefig + "_PlotAmeliorationBN_" + filetime_name + ".png"
        print(filename, " saved on ", os.getcwd())
        plt.savefig(filename)

    plt.show()
    
    return QcRList_set
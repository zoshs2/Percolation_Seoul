import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt
import networkx as nx
from datetime import datetime

def SinglePP(NodeLinkDF:pd.DataFrame, time_dataset:pd.DataFrame, q_step=False, plot=False, savefig:'file_name'=False, verbose=True) -> 'Critical Point value':
    '''
    Extract the critical threshold point by searching over the whole ratio values, sequentially.
    Option[1]: Display a single Percolation Process(PP) for the certain time when we want to observe.
    
    Parameter
    -----------
    NodeLinkDF: pd.DataFrame
        DataFrame which contains pairs with "Start & End Node" for each Seoul Links.
    
    time_dataset: pd.DataFrame
        DataFrame which contains "Link Quality(ratio)" for each Seoul Links.

    q_step: int
        Interval for Link Quality, which used to search the critical threshold point.
        In order to get a more precise result, just leave it as being default (But it is highly time-consuming).

    plot: bool
        On / Off for displaying the Percolation Process(PP).
    
    '''

    if 'ratio' not in time_dataset.columns:
        return print("Your velocity dataframe does not have a 'ratio' column.")
    
    TIME = time_dataset.loc[0, ['PRCS_YEAR', 'PRCS_MON', 'PRCS_DAY', 'PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    TIME = datetime(TIME[0], TIME[1], TIME[2], TIME[3], TIME[4])
    YEAR_MON_DAY = TIME.strftime("%Y-%m-%d")
    filetime_name = str(TIME.strftime("%Y%m%d_%H%M%p"))
    HOUR_MIN = TIME.strftime("%H:%M %p") # %p indicates whether the time on AM or PM.
    
    q_range = time_dataset['ratio'].sort_values().dropna().unique()
    if q_step is not False:
        q_range = q_range[::q_step]
        
    G_size = []
    SG_size = []
    for q in q_range:
        diluted_vel = time_dataset[time_dataset['ratio']>=q].reset_index(drop=True)
        diluted_NL = NodeLinkDF[NodeLinkDF['link_id'].isin(diluted_vel['LINK_ID'].values)]
        st_node = diluted_NL['st_node_nm'].values
        ed_node = diluted_NL['ed_node_nm'].values
        diluted_graph = nx.DiGraph()
        diluted_graph.add_edges_from(zip(st_node, ed_node))
        
        scc_list = []
        for scc in nx.strongly_connected_components(diluted_graph):
            scc_list.append(scc)

        scc_list.sort(key=len, reverse=True)
        G_size.append(len(scc_list[0]))
        SG_size.append(len(scc_list[1]))
    
    qSGset = list(zip(q_range, SG_size))
    qSGset.sort(key=lambda x: x[1], reverse=True)
    critical_point = qSGset[0][0] # Critical point 'q(ratio)' where Second Giant Component size is maximal.
    if verbose is True:
        print(YEAR_MON_DAY, HOUR_MIN, end=' >> ')
        print("Critical Point q_c:", critical_point)
    
    CRITICAL_Qc = r'$q_{c} = $' + str(round(critical_point, 3)) # Displayed q_c is rounded off.

    if plot is True:
        fig, G_ax = plt.subplots(facecolor='w', figsize=(7,7))
        SG_ax = G_ax.twinx()
        G_plot = G_ax.plot(q_range, G_size, markersize=10, c='green', marker="s", alpha=0.8, label='G')
        SG_plot = SG_ax.plot(q_range, SG_size, markersize=10, c='orange', marker="o", alpha=0.8, label='SG')

        x0, xmax = G_ax.get_xlim()
        y0, ymax = G_ax.get_ylim()
        data_width = xmax - x0
        data_height = ymax - y0
        G_ax.text(x0 + data_width * 0.05, y0 + data_height * 0.5, YEAR_MON_DAY, size=23, fontweight='semibold', fontstyle='italic')
        G_ax.text(x0 + data_width * 0.05, y0 + data_height * 0.43, HOUR_MIN, size=23, fontweight='semibold', fontstyle='italic')
        G_ax.text(x0 + data_width * 0.05, y0 + data_height * 0.37, CRITICAL_Qc, size=20, fontweight='semibold', fontstyle='italic')

        lns = G_plot + SG_plot
        labs = [l.get_label() for l in lns]
        G_ax.legend(lns, labs, loc='upper right')
        G_ax.set_xlabel('q')
        G_ax.set_ylabel('G')
        SG_ax.set_ylabel('SG')
        if savefig is not False:
            filename = savefig + "_SinglePP_" + filetime_name + ".png"
            print(filename, " saved on ", os.getcwd())
            plt.savefig(filename)
        plt.show()
        
    return critical_point
def PlotBnOcc(BnOcc, NodeLink, PosDF, ranked=10):
    '''
    Display top-ranked bottleneckes in terms of their occurences, for each peak periods.
    '''
    MorningRank = np.array(sorted(BN_Occ.items(), key= lambda key_val: list(key_val[1].values())[0], reverse=True)[:ranked])
    NoonRank = np.array(sorted(BN_Occ.items(), key= lambda key_val: list(key_val[1].values())[1], reverse=True)[:ranked])
    EveningRank = np.array(sorted(BN_Occ.items(), key= lambda key_val: list(key_val[1].values())[2], reverse=True)[:ranked])
    RankedBN = np.concatenate((MorningRank, NoonRank, EveningRank)).reshape((3, ranked, 2))

    fig = plt.figure(facecolor='w', figsize=(10,10))
    st_node = NodeLink['st_node_nm'].values
    ed_node = NodeLink['ed_node_nm'].values
    graph = nx.DiGraph()
    graph.add_edges_from(zip(st_node, ed_node))
    nx.draw_networkx_nodes(graph, pos=PosDF, node_color='grey', node_size=30, alpha=0.25)
    nx.draw_networkx_edges(graph, pos=PosDF, arrows=False, edge_color='grey', alpha=0.25)

    color = ['red', 'green', 'blue']
    for i, Peak_BN in enumerate(RankedBN):
        PeakNodeDF = NodeLink[NodeLink['link_id'].isin(Peak_BN[:,0])]

        subgraph = nx.DiGraph()
        st_node = PeakNodeDF['st_node_nm'].values
        ed_node = PeakNodeDF['ed_node_nm'].values
        subgraph.add_edges_from(zip(st_node, ed_node))
        nx.draw_networkx_nodes(subgraph, pos=PosDF, node_color=color[i], node_size=1, linewidths=1)
        nx.draw_networkx_edges(subgraph, pos=PosDF, arrows=True, arrowsize=20, arrowstyle='simple', edge_color=color[i])
        nx.draw_networkx_edges(subgraph, pos=PosDF, arrows=False, edge_color=color[i])
    
    plt.show()
def PlotSCCNetwork(q, NodeLink, time_dataset, PosDF, N_scc=3, at_q=False, savefig:'file_name'=False):
    # Make the original network be diluted by link failure that all link having lower than a certain 'threshold(q)' are removed.
    if 'ratio' not in time_dataset.columns:
        raise Warning("time_dataset must include a link quality data column, which is here named after 'ratio'.")

    if N_scc > 5:
        raise KeyError("The number of displayed SCC should be less than or equal to 5.")

    TIME = time_dataset.loc[0, ['PRCS_YEAR','PRCS_MON','PRCS_DAY','PRCS_HH', 'PRCS_MIN']].astype(np.int64).values
    TIME = datetime(TIME[0], TIME[1], TIME[2], TIME[3], TIME[4])
    filetime_name = str(TIME.strftime("%Y%m%d_%H%M%p"))
    YMDHM = TIME.strftime("%Y-%m-%d / %H:%M %p")
    THRESHOLD_TEXT = 'q = ' + str(round(q, 5))

    if at_q is True:
        # Background Nodes
        fig = plt.figure(facecolor='w', figsize=(10,10))

        st_node = NodeLink['st_node_nm'].values
        ed_node = NodeLink['ed_node_nm'].values
        graph = nx.DiGraph()
        graph.add_edges_from(zip(st_node, ed_node))
        nx.draw_networkx_nodes(graph, pos=PosDF, node_color='grey', node_size=30, alpha=0.65)
        nx.draw_networkx_edges(graph, pos=PosDF, arrows=False, edge_color='grey', alpha=0.65)
        
        # Only an Edge having q ratio.
        subgraph = nx.DiGraph()
        Q_NodeLink = NodeLink[NodeLink['link_id']==time_dataset[time_dataset['ratio']==q]['LINK_ID'].values[0]]
        subgraph.add_edges_from(zip(Q_NodeLink['st_node_nm'].values, Q_NodeLink['ed_node_nm']))
        nx.draw_networkx_nodes(subgraph, pos=PosDF, node_color='red', node_size=50, linewidths=1)
        nx.draw_networkx_edges(subgraph, pos=PosDF, arrows=True, arrowsize=10, arrowstyle='simple', width=3, edge_color='red')
        nx.draw_networkx_edges(subgraph, pos=PosDF, arrows=False, width=3, edge_color='blue')

        if savefig is not False:
            filename = savefig + "_SCCNetwork_atQ" + filetime_name + ".png"
            print(filename, " saved on ", os.getcwd())
            plt.savefig(filename)

        plt.show()
        return 

    time_dataset = time_dataset[time_dataset['ratio']>=q]
    NodeLink = NodeLink[NodeLink['link_id'].isin(time_dataset['LINK_ID'])]

    st_node = NodeLink['st_node_nm'].values
    ed_node = NodeLink['ed_node_nm'].values

    # Create the whole corresponding diluted network.
    graph = nx.DiGraph()
    graph.add_edges_from(zip(st_node, ed_node))
    graph_nodes = graph.nodes

    # Extract Strongly Connected Components(SCCs) list.
    comp_list = [c for c in sorted(nx.strongly_connected_components(graph), key=len, reverse=True)]
    
    fig = plt.figure(facecolor='w', figsize=(10,10))
    c_map = ['red', 'blue', 'green', 'purple', 'yellow']

    for i in range(N_scc):
        comp_nodes = comp_list[i]
        graph_nodes = graph_nodes - comp_nodes
    
    else:
        nx.draw_networkx_nodes(graph, pos=PosDF, nodelist=graph_nodes, node_color='grey', node_size=50, alpha=0.3)

    for i in reversed(range(N_scc)):
        comp_nodes = comp_list[i]
        graph_nodes = graph_nodes - comp_nodes # 이 라인은 뭐지? 왜있는거지.
        color = c_map[i]
        
        # Create each scc's subgraph.
        subgraph = nx.DiGraph()
        SubNodes = NodeLink[NodeLink['st_node_nm'].isin(comp_nodes) & NodeLink['ed_node_nm'].isin(comp_nodes)]
        Sub_StNode = SubNodes['st_node_nm'].values
        Sub_EdNode = SubNodes['ed_node_nm'].values
        subgraph.add_edges_from(zip(Sub_StNode, Sub_EdNode))
        
        # Draw SCC's subgraph.
        nx.draw_networkx_nodes(subgraph, pos=PosDF, node_color=color, node_size=50, linewidths=1)
        nx.draw_networkx_edges(subgraph, pos=PosDF, arrows=False)
        
    plt.text(126.8, 37.685, YMDHM, size=20, fontweight='semibold', fontstyle='italic')
    plt.text(126.8, 37.670, THRESHOLD_TEXT, size=20, fontweight='semibold', fontstyle='italic')

    if savefig is not False:
        filename = savefig + "_SCCNetwork_" + filetime_name + ".png"
        print(filename, " saved on ", os.getcwd())
        plt.savefig(filename)
    
    plt.show()
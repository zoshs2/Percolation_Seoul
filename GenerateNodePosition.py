def GenerateNodePosition(NodeLinkDF, LinkLocationDF):
    NodeLinkDF = NodeLinkDF[NodeLinkDF['link_id'].isin(LinkLocationDF['link_id'].unique())].reset_index(drop=True)
    Node_Position = {}

    st_grouped = LinkLocationDF.groupby('link_id').nth(0).reset_index()
    ed_grouped = LinkLocationDF.groupby('link_id').nth(-1).reset_index()
    st_lonlat_series = st_grouped.loc[:,['lon','lat']]
    ed_lonlat_series = ed_grouped.loc[:,['lon','lat']]

    PositionPack = list(zip(list(zip(list(zip(st_lonlat_series.lon, st_lonlat_series.lat)), list(zip(ed_lonlat_series.lon, ed_lonlat_series.lat)))), list(zip(NodeLinkDF.st_node_nm, NodeLinkDF.ed_node_nm))))

    for lonlat, nodes in PositionPack:
        for i, node in enumerate(nodes):
            if node in PositionPack:
                continue
            
            Node_Position[node] = lonlat[i]

    return Node_Position
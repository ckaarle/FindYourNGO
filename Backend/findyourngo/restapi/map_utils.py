def get_links_between_ngos(clusters, ngos, connections):
    clustered_ngos: {int: int} = {}
    without_coordinates = 0
    unassigned = 0
    for ngo in ngos:
        lat = ngo.contact.address.latitude
        long = ngo.contact.address.longitude
        if not (lat and lat != '""' and long and long != '""'):
            # print(f'Ngo {ngo.name} has no registered coordinates! Excluding from calculation')
            without_coordinates += 1
            continue
        lat = float(lat)
        long = float(long)
        for cluster in clusters:
            if float(cluster['lat_min']) <= lat <= float(cluster['lat_max']) \
                    and float(cluster['lng_min']) <= long <= float(cluster['lng_max']):
                clustered_ngos[ngo.id] = int(cluster['id'])
                break
        else:
            # print(f'Ngo {ngo.name} in {lat}, {long} could not be assigned to any cluster')
            unassigned += 1
    print(f'{without_coordinates} ngos had no coordinates and {unassigned} ngos could not be assigned to any cluster')

    link_count = {}
    for cluster1 in clusters:
        for cluster2 in clusters:
            if int(cluster1['id']) < int(cluster2['id']):
                link_count[(int(cluster1['id']), int(cluster2['id']))] = 0
    for connection in connections:
        rep_id = connection.reporter_id
        con_id = connection.connected_ngo_id
        if rep_id != con_id and rep_id in clustered_ngos and con_id in clustered_ngos \
                and clustered_ngos[rep_id] < clustered_ngos[con_id]:
            cluster1 = clustered_ngos[rep_id]
            cluster2 = clustered_ngos[con_id]
            link_count[(cluster1, cluster2)] += 1
    return link_count

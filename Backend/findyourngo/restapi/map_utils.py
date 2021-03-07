def get_links_between_ngos(clusters, ngos, connections):
    clustered_ngos: {int: int} = {}  # ngo to cluster mapping
    without_coordinates = 0
    unassigned = 0
    clusters = {cluster['id']: cluster for cluster in clusters}
    ordered_ngos = {}
    for ngo in ngos:
        ordered_ngos[ngo.id] = ngo
        if ngo.contact.address is None:
            without_coordinates += 1
            continue
        lat = ngo.contact.address.latitude
        long = ngo.contact.address.longitude
        if not (lat and lat != '""' and long and long != '""'):
            # print(f'Ngo {ngo.name} has no registered coordinates! Excluding from calculation')
            without_coordinates += 1
            clustered_ngos[ngo.id] = 'without_coordinates'
            continue
        for cluster in clusters.values():
            if float(cluster['lat_min']) - 0.001 <= float(lat) <= float(cluster['lat_max']) + 0.001 \
                    and float(cluster['lng_min']) - 0.001 <= float(long) <= float(cluster['lng_max']) + 0.001:
                clustered_ngos[ngo.id] = int(cluster['id'])
                break
        else:
            # print(f'Ngo {ngo.name} in {lat}, {long} could not be assigned to any cluster')
            clustered_ngos[ngo.id] = 'unassigned'
            unassigned += 1  # if unassigned, assign at the end!
    print(f'{without_coordinates} ngos had no coordinates and {unassigned} ngos could not be assigned to any cluster')
    # print('Length of clustered_ngos', len(clustered_ngos))

    link_count = {}
    location_link_count = {}
    out_of_view_count = 0
    for cluster1 in clusters.values():
        for cluster2 in clusters.values():
            if int(cluster1['id']) < int(cluster2['id']):
                link_count[(int(cluster1['id']), int(cluster2['id']))] = 0
    for connection in connections:
        rep_id = connection.reporter_id
        con_id = connection.connected_ngo_id
        if clustered_ngos[rep_id] == 'without_coordinates' or clustered_ngos[con_id] == 'without_coordinates':
            out_of_view_count += 1
            continue
        if clustered_ngos[rep_id] == 'unassigned' and clustered_ngos[con_id] == 'unassigned':
            out_of_view_count += 1
            continue
        if clustered_ngos[rep_id] == 'unassigned':
            known_cluster = clusters[clustered_ngos[con_id]]
            lat = float(ordered_ngos[rep_id].contact.address.latitude)
            long = float(ordered_ngos[rep_id].contact.address.longitude)
            con = (calculate_coordinates(known_cluster), (long, lat))
            if location_link_count.get(con):
                location_link_count[con] += 1
            else:
                location_link_count[con] = 1
            continue
        if clustered_ngos[con_id] == 'unassigned':
            continue
        if rep_id != con_id and rep_id in clustered_ngos and con_id in clustered_ngos \
                and clustered_ngos[rep_id] < clustered_ngos[con_id]:
            cluster1 = clustered_ngos[rep_id]
            cluster2 = clustered_ngos[con_id]
            link_count[(cluster1, cluster2)] += 1
    for ((x, y), z) in link_count.items():
        if (x, y) in location_link_count:
            print(f"Warning, {(x, y)} was already in location_link_count, which shouldn't have happened")
        location_link_count[(calculate_coordinates(clusters[x]), calculate_coordinates(clusters[y]))] = z
    return location_link_count


def calculate_coordinates(cluster):
    latitude = float(cluster['lat_min']) + float(cluster['lat_max'])
    longtitude = float(cluster['lng_min']) + float(cluster['lng_max'])
    return longtitude / 2, latitude / 2

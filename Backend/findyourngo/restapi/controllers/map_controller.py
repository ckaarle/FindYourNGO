import requests

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from urllib.parse import unquote_plus
from rest_framework.parsers import JSONParser

import json

from findyourngo.restapi.models import Ngo, NgoConnection, NgoAddress
from findyourngo.restapi.serializers.ngo_serializer import NgoPlotSerializer, NgoLinkSerializer


@api_view(['GET'])
def get_plots(request) -> JsonResponse:
    plot_serializer = NgoPlotSerializer(Ngo.objects.all()[:200], many=True)
    return JsonResponse(plot_serializer.data, safe=False)


@api_view(['POST'])
def get_links(request) -> JsonResponse:
    clusters = JSONParser().parse(request)['clusters']
    if clusters:
        ngo_links = get_links_between_ngos(clusters, Ngo.objects.all(), NgoConnection.objects.all())
        return JsonResponse([{'id1': c1, 'id2': c2, 'link_count': count} for ((c1, c2), count) in ngo_links.items()],
                            safe=False)

    link_serializer = NgoLinkSerializer(NgoConnection.objects.all(), many=True)
    return JsonResponse(link_serializer.data, safe=False)


def get_links_between_ngos(clusters, ngos, connections):
    clustered_ngos: {int: int} = {}
    for ngo in ngos:
            lat = float(ngo.contact.address.latitude)
            long = float(ngo.contact.address.longitude)
        if not (lat and long):
            print(f'Ngo {ngo.name} has no registered coordinates! Excluding from calculation')
            continue
        for cluster in clusters:
            if float(cluster['lat_min']) <= lat <= float(cluster['lat_max']) \
                    and float(cluster['lng_min']) <= long <= float(cluster['lng_max']):
                clustered_ngos[ngo.id] = int(cluster['id'])
                break
        else:
            print(f'Ngo {ngo.name} in {lat}, {long} could not be assigned to any cluster')

    link_count = {}
    for cluster1 in clusters:
        for cluster2 in clusters:
            if int(cluster1['id']) < int(cluster2['id']):
                link_count[(int(cluster1['id']), int(cluster2['id']))] = 0
    for connection in connections:
        rep_id = connection.reporter_id
        con_id = connection.connected_ngo_id
        if rep_id < con_id and rep_id in clustered_ngos and con_id in clustered_ngos \
                and clustered_ngos[rep_id] != clustered_ngos[con_id]:
            cluster1 = clustered_ngos[rep_id]
            cluster2 = clustered_ngos[con_id]
            link_count[(cluster1, cluster2)] += 1
    return link_count


@api_view(['GET'])
def update_geo_locations(request) -> JsonResponse:
    reuse_csv_data()
    # If you want to refresh all addresses, use the following method
    # for address in NgoAddress.objects.all():
    #     geo_locate_single_address(address)
    return JsonResponse({'success': 'NGOs relocated successfully'})


def reuse_csv_data():
    pass
    with open('findyourngo/data_import/ngo_geo.csv', 'r') as f:
        for line in f:
            props = line.strip().rsplit(',', 2)
            if props[0] == 'name':
                continue
            try:
                # some addresses are shared, which means they will be updated multiple times,
                # but this shouldn't cause too much of a performance hit
                address = Ngo.objects.get(name=props[0]).contact.address
                address.latitude = props[1]
                address.longitude = props[2]
                address.save()
            except:
                print('Failed to locate address for', props[0])


def geo_locate_single_address(address: NgoAddress):
    api_key = 'AIzaSyAjGMTYr5XRGE98NhWeAvKj3qa_e9j7Pk4'
    address_string = ''

    def parse(elem):
        if elem.strip() != '':
            return elem.strip().replace(' ', '+') + '+'
        return ''

    address_string += parse(address.street)
    address_string += parse(address.postcode)
    address_string += parse(address.city)

    print("Current address " + address_string)

    if address_string == '':
        address.latitude = ''
        address.longitude = ''
        address.save()
    else:
        address_string += parse(address.country.name)
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_string}&key={api_key}'
        location = requests.get(url).json()['results'][0]['geometry']['location']
        print(location['lat'], location['lng'])
        address.latitude = location['lat']
        address.longitude = location['lng']
        address.save()

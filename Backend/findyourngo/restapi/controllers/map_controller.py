import random

import requests

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from findyourngo.restapi.models import Ngo, NgoConnection, NgoAddress
from findyourngo.restapi.serializers.ngo_serializer import NgoPlotSerializer, NgoLinkSerializer
from findyourngo.restapi.map_utils import get_links_between_ngos


@api_view(['GET'])
def get_plots(request) -> JsonResponse:
    plot_serializer = NgoPlotSerializer(Ngo.objects.filter(
        confirmed=True, contact__address__country__isnull=False
    ).select_related('contact__address'), many=True)
    result = [plot for plot in plot_serializer.data if plot['coordinates'][0] != '""' and plot['coordinates'][1] != '""']
    return JsonResponse(result, safe=False)


@api_view(['POST'])
def get_links(request) -> JsonResponse:
    clusters = JSONParser().parse(request)['clusters']
    if clusters:
        ngo_links = get_links_between_ngos(
            clusters, Ngo.objects.filter(confirmed=True, connected_ngo__isnull=False).distinct().select_related('contact__address'),
            NgoConnection.objects.all().select_related(
                'connected_ngo__contact__address', 'reporter__contact__address'))
        return JsonResponse([{'origin': c1, 'destination': c2, 'link_count': count} for ((c1, c2), count) in
                             ngo_links.items() if count > 0], safe=False)

    link_serializer = NgoLinkSerializer(NgoConnection.objects.all(), many=True)
    return JsonResponse(link_serializer.data, safe=False)


@api_view(['GET'])
def update_geo_locations(request) -> JsonResponse:
    update_geo_locations_logic()
    return JsonResponse({'success': 'NGOs relocated successfully'})


def update_geo_locations_logic():
    reuse_csv_data()
    # If you want to refresh all addresses, use the following method
    # for address in NgoAddress.objects.all():
    #     geo_locate_single_address(address)
    assign_probable_locations()


def reuse_csv_data():
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


def assign_probable_locations():
    coordinates = {}
    with open('findyourngo/data_import/coordinates.csv', 'r') as f:
        for line in f:
            props = line.upper().split(',')
            coordinates[props[3].strip()] = (props[1], props[2])

    ngos = Ngo.objects.filter(confirmed=True, contact__address__country__isnull=False, contact__address__latitude=''
                              ).select_related('contact__address')

    for ngo in ngos:
        lat = ngo.contact.address.latitude
        long = ngo.contact.address.longitude
        if lat and long and lat != '""' and long != '""':
            return lat, long

        lat = float(coordinates[ngo.contact.address.country.name][0]) + random.uniform(-0.05, 0.05)
        long = float(coordinates[ngo.contact.address.country.name][1]) + random.uniform(-0.05, 0.05)
        # save lat and long after assigning it randomly
        ngo.contact.address.latitude = lat
        ngo.contact.address.longitude = long
        ngo.contact.address.save()

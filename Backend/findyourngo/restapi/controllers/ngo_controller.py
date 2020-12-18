from typing import Any

from django.db.models import QuerySet
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.filtering.NgoFilter import NgoFilter
from findyourngo.restapi.models import Ngo, NgoTopic, NgoBranch, NgoAddress, NgoType, NgoStats
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer, filter_object
from findyourngo.restapi.serializers.ngo_serializer import NgoSerializer


@api_view(['GET', 'POST', 'DELETE'])
def ngo_list(request):
    if request.method == 'GET':
        ngos = Ngo.objects.all()

        # TODO: any conditions?

        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)

    elif request.method == 'POST':
        ngo_data = JSONParser().parse(request)
        ngo_serializer = NgoSerializer(data=ngo_data)
        if ngo_serializer.is_valid():
            ngo_serializer.save()
            return JsonResponse(ngo_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ngo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ngo_detail(request, pk):
    ngo = Ngo.objects.get(pk=pk)

    if request.method == 'GET':
        ngo_serializer = NgoSerializer(ngo)
        return JsonResponse(ngo_serializer.data)

    elif request.method == 'PUT':
        ngo_data = JSONParser().parse(request)
        ngo_serializer = NgoSerializer(ngo, data=ngo_data)
        if ngo_serializer.is_valid():
            ngo_serializer.save()
            return JsonResponse(ngo_serializer.data)
        return JsonResponse(ngo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ngo.delete()
        return JsonResponse({'message': 'Ngo was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ngo_filter_options(request: Any) -> JsonResponse:
    return JsonResponse(filter_object())

def filter_object():  # TODO: move to frontend
    return {
        'branches': {"displayName": "Branches", "values": branches(), "icon": "account_tree"},
        'topics': {"displayName": "Topics", "values": topics(), "icon": "topic"},
        'hasEcosoc': {"displayName": "Accreditations", "values": False, "icon": "account_balance"},
        'isCredible': {"displayName": "Credibility", "values": False, "icon": "loyalty"},
        'countries': {"displayName": "Countries", "values": hq_countries(), "icon": "flag"},
        'cities': {"displayName": "Cities", "values": None, "icon": "location_on"},
        'contactOptionPresent': {"displayName": "Contactable", "values": False, "icon": "how_to_reg"},
        'typeOfOrganization': {"displayName": "Type of organization", "values": types_of_organization(),
                               "icon": "corporate_fare"},
        'workingLanguages': {"displayName": "Working languages", "values": working_languages(),
                             "icon": "translate"},
        'funding': {"displayName": "Funding", "values": funding(), "icon": "attach_money"},
        'trustworthiness': {"displayName": "Trustworthiness", "values": None, "icon": "star"}
    }

def branches():
    branches = list(map(lambda ngo_branch: ngo_branch['country'],
                        NgoBranch.objects.all().order_by('country').values('country').distinct()))
    return branches

def topics():
    topics = list(map(lambda ngo_topic: ngo_topic['topic'],
                      NgoTopic.objects.all().order_by('topic').values('topic').distinct()))
    return topics

def hq_countries():
    hq_countries = list(map(lambda ngo_hq_address: ngo_hq_address['country'],
                            NgoAddress.objects.all().order_by('country').values('country').distinct()))
    return hq_countries

def types_of_organization():
    types_of_organization = list(
        map(lambda ngo_type: ngo_type['type'], NgoType.objects.all().order_by('type').values('type').distinct()))
    return types_of_organization

def working_languages():
    return ["English", "French", "German"]

def funding():
    funding = list(map(lambda ngo_stats: ngo_stats['funding'],
                       NgoStats.objects.all().order_by('funding').values('funding').distinct()))
    return funding

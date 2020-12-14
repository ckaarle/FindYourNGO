from django.db.models import QuerySet
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.filtering.NgoFilter import NgoFilter
from findyourngo.restapi.models import Ngo, NgoTopic, NgoBranch, NgoAddress, NgoType, NgoStats
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer
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

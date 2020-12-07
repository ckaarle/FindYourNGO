from typing import List

from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.filtering.Filter import Filter
from findyourngo.filtering.filter_util import FilterConfig
from findyourngo.restapi.models import Ngo
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer
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


@api_view(['POST', 'GET'])
def ngo_filter(request):
    # TODO just for testing, remove later
    if request.method == 'GET':
        filter_config = FilterConfig(use_ecosoc=True, branches_to_include=['ALBANIA'])
        filter = Filter(filter_config)
        ngo_result: List[Ngo] = filter.apply()

        result_serializer = NgoSerializer(ngo_result, many=True)

        return JsonResponse(result_serializer.data, safe=False)
    # TODO end remove later

    filter_data = JSONParser().parse(request)
    filter_serializer = FilterSerializer(data=filter_data)

    if filter_serializer.is_valid():
        filter_config = filter_serializer.create(filter_serializer.validated_data)
        filter = Filter(filter_config)
        ngo_result: List[Ngo] = filter.apply()

        result_serializer = NgoSerializer(ngo_result, many=True)

        return JsonResponse(result_serializer.data, safe=False)

    return JsonResponse(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

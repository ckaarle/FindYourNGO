from typing import Any

from django.db.models import QuerySet
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from urllib.parse import unquote_plus
import json

from findyourngo.filtering.NgoFilter import NgoFilter
from findyourngo.restapi.paginators.NgoOverviewItemListPaginator import NgoOverviewItemListPaginator
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer, filter_object
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer

MAX_PAGE_SIZE = 20

@api_view(['GET'])
def ngo_filter_options(request: Any) -> JsonResponse:
    return JsonResponse(filter_object())


@api_view(['GET'])
def filter_options(request: Any) -> JsonResponse:
    filter_data = json.loads(unquote_plus(request.query_params.get('filter_selection')))
    filter_serializer = FilterSerializer(data=filter_data)

    if filter_serializer.is_valid():
        filter_serializer = filter_serializer.create(filter_serializer.validated_data)
    else:
        return JsonResponse(filter_serializer, status=status.HTTP_400_BAD_REQUEST)

    paginator = NgoOverviewItemListPaginator()
    paginator.page_size = MAX_PAGE_SIZE

    filters = NgoFilter(filter_serializer)
    queryset: QuerySet = filters.apply()

    result_page = paginator.paginate_queryset(queryset, request)

    ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
    return paginator.get_paginated_response(ngo_overview_item_serializer.data)

